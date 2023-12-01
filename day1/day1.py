import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utils.time_run import log_time
from utils.loc import recurse_dir

def data_load(filen:str)->list:
	with open(f'./day1/{filen}.txt', 'r') as f:
		data = f.read().splitlines()
		arr = [x if x != "" else "" for x in data]
	return arr

def extract_calibration(data:list)->list:
	calibrations = []
	for line in data:
		temp = []
		#Check if each character in a line is numeric. 
		#if so add to temp list as a tuple of (number, pos)
		for idx, ch in enumerate(line):
			if ch.isdigit():
				temp.append((ch, idx))
		#sort the list
		sortme = sorted(temp, key=lambda x:x[1])
		#Take the first and last as your numbers
		calibrations.append(int(f'{sortme[0][0]}{sortme[-1][0]}'))
	return calibrations

def find_all(key:str, line:str)-> int:
	"""When you index a string or group of strings
	you will get the first occurance returned.  But there
	could be a situation where there's another of the same 
	number string at the end of the string.  This generator
	function will return all indexes of where that number
	occurs in a string.

	Args:
		key (str): number we're looking for
		line (str): full string of the each line in the dataset

	Yields:
		idx (int): position
	"""	
	idx = line.find(key)
	while idx != -1:
		yield idx
		idx = line.find(key, idx+1)

def extract_updated(data:list)->list:
	calibrations = []
	num_dict = {
		"one":1,
		"two":2,
		"three":3,
		"four":4,
		"five":5, 
		"six":6,
		"seven":7,
		"eight":8,
		"nine":9
	}
	for line in data:
		temp = []
		#Iterate the num_dict keys to see if they exist in each line
		for key in num_dict.keys():
			if key in line:
				#Now find all occurances of each key and add them as a tuple to the temp list
				[temp.append((num_dict[line[x:x+len(key)]], x)) for x in find_all(key, line)]

		#iterate each character in the line to check for numerics
		#Add the number and its index as a tuple
		#Sort the tuples.  Take the first and last
		for idx, ch in enumerate(line):
			if ch.isdigit():
				temp.append((int(ch), idx))
		sortme = sorted(temp, key=lambda x:x[1])
		calibrations.append(int(f"{sortme[0][0]}{sortme[-1][0]}"))
	return calibrations

@log_time
def run_part_A():
	data = data_load("test_data1")
	calibrations = extract_calibration(data)
	return sum(calibrations)
#Part A Notes
#Nice easy snowball to start
#Our job is to combine the first and last int found in each string. 
#return their sum

@log_time
def run_part_B():
	data = data_load("test_data2")
	calibrations = extract_updated(data)
	return sum(calibrations)
#Part B Notes
#Little more complicated but now numbers spelled out 1-9 as text count
	
print(f"Part A solution: \n{run_part_A()}\n")
print(f"Part B solution: \n{run_part_B()}\n")
print(f"Lines of code \n{recurse_dir('./day1/')}")
