# Anthony Vigil and Oguz Yetkin

from math import exp
from random import random
import serial
import sys
import os
import time


def fun(filename, arr):
    serial_port='COM7'
    ser = serial.Serial(serial_port,115200)
    #arr = ['open','close']
    for i in range(0,3):
        for j in range(len(arr)):
            file = open('Testing.txt','w')
            print('\nPlease sign '+arr[j]+' gesture.\nRecording Begins in:')
            time.sleep(1)
            print("3"),
            print('... ')
            time.sleep(1)
            print('2'),
            print('... ')
            time.sleep(1)
            print('1')
            time.sleep(1)
            print('Recording started')
            timeend = time.time() + 10
            while True:
                try:
                    file.write(ser.readline().decode('utf-8'))
                    sys.stdout.flush()
                    if timeend < time.time():
                        file.close()
                        break
                except KeyboardInterrupt:
                    file.close()
                    break
			#Preprocessing Data
            max_value = filelength('Testing.txt')
            #print("max ="+str(max_value))
            with open('Testing.txt', 'r') as f:
                lines = f.readlines()
            with open(filename, 'a') as f:
                for line in lines:
                    #print("length= "+str(len(line)))
                    if len(line) == max_value:
                        line = line[:-2] + " " +str(j) +line[-1] #add gesture number
                        temp = [float(num) for num in line.split()]
                        #print("len"+str(len(temp)))
                        if len(temp) == 226: #check for the complete line
                            f.write(line)

	#f.close()
	#os.remove("Testing.txt")
	#print('Hello')


def filelength(filename):
	unique_char = []
	unique_fr = []
	temp_filechar = []
	with open(filename, 'r') as f:
		for line in f:
			temp = len(line)
			if temp != 1:
				temp_filechar.append(temp)
	fr = [None]*len(temp_filechar)
	visited = -1
	for i in range(0,len(temp_filechar)):
		count = 1
		for j in range(i+1, len(temp_filechar)):
			if (temp_filechar[i] == temp_filechar[j]):
				count = count + 1
				fr[j] = visited
		if(fr[i] != visited):
			fr[i] = count
	for i in range(0,len(fr)):
		if(fr[i] != visited):
			unique_char.append(temp_filechar[i])
			unique_fr.append(fr[i])
	temp = unique_fr.index(max(unique_fr))
	return unique_char[temp]

print('Start Training')
narr = input('Enter numebr of gesture')
arr = []
for i in range(0,int(narr)):
    temp = input('enter name')
    arr.append(temp)
fun('Training_Data.txt', arr)
print('\nEnd Training')
