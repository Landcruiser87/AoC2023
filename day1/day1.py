import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utils.time_run import log_time

def data_load(filen:str)->list:
	# ./day/
	with open(f'./day1/{filen}.txt', 'r') as f:
		data = f.read().splitlines()
		arr = [x if x != "" else "" for x in data]
	return arr

def extract_calibration(data:list)->list:
	calibrations = []
	for line in data:
		temp = []
		for idx, ch in enumerate(line):
			if ch.isdigit():
				temp.append((ch, idx))
		sortme = sorted(temp, key=lambda x:x[1])
		calibrations.append(int(f'{sortme[0][0]}{sortme[-1][0]}'))
	return calibrations

def find_all(key:str, line:str):
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
		for key in num_dict.keys():
			if key in line:
				[temp.append((num_dict[line[x:x+len(key)]], x)) for x in find_all(key, line)]

		for idx, ch in enumerate(line):
			if ch.isdigit():
				temp.append((int(ch), idx))
		sortme = sorted(temp, key=lambda x:x[1])
		calibrations.append(int(f"{sortme[0][0]}{sortme[-1][0]}"))
	return calibrations

@log_time
def run_part_A():
	data = data_load("data")
	calibrations = extract_calibration(data)
	return sum(calibrations)
#Part A Notes
#Nice easy snowball to start
#Our job is to combine the first and last int found in each string. 
#return their sum

@log_time
def run_part_B():
	data = data_load("data")
	calibrations = extract_updated(data)
	return sum(calibrations)
#Part B Notes
#Little more complicated but now numbers spelled out 1-9 as text count
	
print(f"Part A solution: \n{run_part_A()}\n")
print(f"Part B solution: \n{run_part_B()}\n")

