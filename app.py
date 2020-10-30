######################################################################
##########    ffmpeg is required to split the video into partisions
##########    "sudo apt install ffmpeg"
##########    Run the above command to install ffmpeg in linux
######################################################################

import multiprocessing
import subprocess
import time
import os

filename = "video/gintama.mp4"
parts_size_time = 1 # in minuts

parts_size_time = parts_size_time*60

def video_duration(filename):
    import subprocess
    secs = subprocess.check_output(f'ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 "{filename}"', shell=True).decode()
    return secs

def thread_list(list,n):
	splited = []
	len_l = len(list)
	for i in range(n):
		start = int(i*len_l/n)
		end = int((i+1)*len_l/n)
		splited.append(list[start:end])
	return splited

def thread_call(list,ln):
	tmp = 0
	for sub in list:
		cmd = f"ffmpeg -i {filename} -ss {sub[0]} -t {sub[1]} splits/filename-{ln}-tmp.mp4"
		os.system(cmd)
		#subprocess.run(["ffmpeg",cmd])
		# lst = f"splits/filename-{ln}-tmp.m4v"
		# subprocess.run(["ffmpeg","-i", filename, "-ss",sub[0], -t, sub[1],lst])
		tmp += 1
	del tmp



videosize = int(float(video_duration(filename)))

tmp = videosize
ct = 0
list = []
while (ct <= tmp):
	list.append([ct+1,ct+parts_size_time])
	ct = ct+parts_size_time
print(list)
n = int(input("Number of threads to run : "))
if n > len(list):
	n = len(list)
thread_call_list = thread_list(list, n)
threads = []
t1 = time.perf_counter()
a = 1
for sublist in thread_call_list:
	t = multiprocessing.Process(target=thread_call, args=[sublist, a])
	t.start()
	threads.append(t)
	a = a+1
for thread in threads:
	thread.join()
t2 = time.perf_counter()
print(f"Splitting Duration : {round(t2-t1)/60} minutes")