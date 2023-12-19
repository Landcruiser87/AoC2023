import os
import sys
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utils.time_run import log_time
from utils.loc import recurse_dir
import numpy as np
from itertools import combinations

DAY = './day_11/'
def data_load(filen:str)->list:
	with open(f'{DAY}{filen}.txt', 'r') as f:
		data = f.read().splitlines()
		arr = [list(x.strip()) if x != "" else "" for x in data]
	return np.array(arr, dtype=str)

def expand_galaxy(data:list, magnify:int=2):
	temp_data = data.copy()
	col_idx, row_idx = [], []
	step_count = 0

	#Grab the indexes with empty columns
	for row in range(data.shape[0]):
		if "#" not in data[row, :]:
			row_idx.append(row)

	for col in range(data.shape[1]): 
		if "#" not in data[:, col]:
			col_idx.append(col)

	# Extract all indices where == #
	pound_towns = list(zip(np.where(data=="#")[0], np.where(data=="#")[1]))
	# Find all possible combinations of points
	mambo_combo = list(combinations(pound_towns, 2))

	#Calculate the shortest distance for each combinattion
	for (x1,y1),(x2,y2) in mambo_combo:
		#MIght take this out for hte absolutes
		if x1 > x2:
			x1, x2 = x2, x2
		if y1 > y2:
			y1, y2 = y2, y1
		for step in range(x1, x2):
			if step in row_idx:
				step_count += magnify
			else:
				step_count += 1

		for step in range(y1, y2):
			if step in col_idx:
				step_count += magnify
			else:
				step_count += 1

	return step_count	

@log_time
def part_A():
	data = data_load("data")
	count = expand_galaxy(data)
	return count

@log_time
def part_B():
	data = data_load("data")
	count = expand_galaxy(data, 1_000_000)
	return count
	
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
