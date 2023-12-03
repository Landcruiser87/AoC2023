import os
import sys
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from collections import deque
from utils.time_run import log_time
from utils.loc import recurse_dir
DAY = './day3/'

def data_load(filen:str)->list:
	with open(f'{DAY}{filen}.txt', 'r') as f:
		data = f.read().splitlines()
		arr = [x if x != "" else "" for x in data]
	return arr

def get_full_num(data:list, loc:tuple)->int:
	row = loc[0]
	col = loc[1]
	idxleft, idxright = 0, 0
	#BUG has to be here. 
	while (data[row][col+idxleft].isnumeric()) and (not col+idxleft <= 0):
		idxleft -= 1  
	while data[row][col+idxright].isnumeric() and col+idxright <= len(data[row]):
		idxright += 1
	
	temp = data[row][col+idxleft:col+idxright]
	temp = "".join([x for x in temp if x.isalnum()])
	return int(temp)

def adjacent_nums(data, char_idx:list):
	x_ran = range(-1, 2)
	y_ran = range(-1, 2)
	full_num = []
	char_pile = deque(char_idx)
	#Iterate the rows and look for numbers. 
	while char_pile:
		char = char_pile.popleft()
		for row in x_ran:
			for col in y_ran:
				if data[char[0]+row][char[1]+col].isnumeric():
					temp_num = get_full_num(data, (char[0]+row, char[1]+col))
					if temp_num not in full_num:
						full_num.append(temp_num)
	return full_num

def engine_parts(data:list, part:str)->list:
	char_idxs = []
	#Iterate the grid
	for row in data:
		for ch in row:
			#test to see if the value is numeric or not a period.
			#Should trap all characters we want
			#append their tuple locaton to char_idxs
			if (not ch.isnumeric()) and (ch != "."):
				char_idxs.append((data.index(row), row.index(ch)))

	#Test to see if adjacent numbers have a character neighbor
	part_numbers = adjacent_nums(data, char_idxs)
	return part_numbers

@log_time
def run_part_A():
	data = data_load("data")
	part_numbers = engine_parts(data, "A")
	return sum(part_numbers)

@log_time
def run_part_B():
	data = data_load()
	
print(f"Part A solution: \n{run_part_A()}\n")
# print(f"Part B solution: \n{run_part_B()}\n")
print(f"Lines of code \n{recurse_dir(DAY)}")

########################################################
#Notes
#Part A Notes

#strange puzzle input but we're looking at 
#engine schematics.  Any number that is seated next to an non-alphanumeric
#is a part number.  sum up all the part numbers. 
#need a function to return when a part number is adjacent to a symbol
