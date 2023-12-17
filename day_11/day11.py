import os
import sys
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utils.time_run import log_time
from utils.loc import recurse_dir
import numpy as np
from itertools import combinations
from collections import deque


DAY = './day_11/'
def data_load(filen:str)->list:
	with open(f'{DAY}{filen}.txt', 'r') as f:
		data = f.read().splitlines()
		arr = [list(x.strip()) if x != "" else "" for x in data]
	return np.array(arr, dtype=str)

def expand_galaxy(data:list, part:str, magnify:int=100):
	temp_data = data.copy()
	col_idx, row_idx = [], []
	for row in range(data.shape[0]):
		if "#" not in data[row, :]:
			row_idx.append(row)
			
	if part == "A":
		temp_data = np.insert(temp_data, row_idx, "."*temp_data.shape[0], axis = 0)
	else:
		input_arr = np.repeat(".", temp_data.shape[0]*magnify).reshape(magnify, -1)
		shift = 0
		for row in row_idx:
			# print(temp_data[:row+shift, :], "\n")
			# print(input_arr[:-1], "\n")
			# print(temp_data[row+shift:, :], "\n")
			temp_data = np.vstack([
				temp_data[:row+shift, :],
				input_arr[:-1],
				temp_data[row+shift:, :]
			])
			shift += magnify - 1
			# print("\n"*8, temp_data,"\n"*2, temp_data.shape)

	for col in range(data.shape[1]): 
		if "#" not in data[:, col]:
			col_idx.append(col)
	if part == "A":
		temp_data = np.insert(temp_data, col_idx, "."*temp_data.shape[1], axis = 1)
	else:

		input_arr = np.repeat(".", temp_data.shape[0]*magnify).reshape(-1, magnify)
		shift = 0
		for col in col_idx:
			# print(temp_data[:, :col+shift], "\n")
			# print(input_arr[:, :-1], "\n")
			# print(temp_data[:, col+shift:], "\n")

			temp_data = np.hstack([
				temp_data[:, :col+shift],
				input_arr[:, :-1], 
				temp_data[:, col+shift:]
			])
			shift += magnify - 1
			# print("\n"*8, temp_data,"\n"*2, temp_data.shape)
	return temp_data	

def calc_manhattan(combo:tuple):
	return np.sum(np.abs(np.array(combo[0])-np.array(combo[1])))

def calculate_paths(data:list, part:str):
	gmap = expand_galaxy(data, part)
	paths = []
	# Extract all indices where == #
	pound_towns = list(zip(np.where(gmap=="#")[0], np.where(gmap=="#")[1]))
	# Find all possible combinations of points
	mambo_combo = list(combinations(pound_towns, 2))
	#Calculate the shortest distance for each 
	for combo in mambo_combo:
		paths.append(calc_manhattan(combo))
	return paths

@log_time
def part_A():
	data = data_load("test_data")
	paths = calculate_paths(data, "A")
	return sum(paths)

@log_time
def part_B():
	low_fails = [78845397]
	high_fails = []
	data = data_load("test_data")
	paths = calculate_paths(data, "B")
	path_sum = sum(paths)
	if path_sum in low_fails: raise ValueError(f"{path_sum} is too low")
	if path_sum in high_fails: raise ValueError(f"{path_sum} is too high")
	return sum(paths)
	
print(f"Part A solution: \n{part_A()}\n")
print(f"Part B solution: \n{part_B()}\n")
print(f"Lines of code \n{recurse_dir(DAY)}")

########################################################
#Notes
#Part A Notes

# First thing to do is expand the galaxy. 
# Those get expanded by however many open rows / cols
# there are that don't contain a # symbol
# add one row/col for each blank you have respectively. 

#Part B

#toolow - 78845397
