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
		arr = [x.strip() if x != "" else "" for x in data]
	return arr


def engine_parts(data:list, part:str)->list:
	left_num_idxs = set()
	part_numbers = []
	#Iterate the grid. If any non alphanumerics found, iterate again in 1 square space.
	#If any numbers are found, Step left to the beginning of the number. 
	#Store numeric location as tuple (row, col)
	for row, line in enumerate(data):
		for col, ch in enumerate(line):
			#If its a digit or period, move on and don't analyze it
			if (ch.isdigit()) | (ch == "."):
				continue

			#If its a nonalphanumeric.  Search nearby coordinates
			for xmov in [row - 1, row, row + 1]:
				for ymov in [col - 1, col, col + 1]:
					# If we didn't violate the grid shape and the number is a digit, continue
					if (xmov < 0) or (xmov >= len(data)) or (ymov < 0) or (ymov >= len(data[xmov])) or not data[xmov][ymov].isdigit():
						continue
					#Step left to find the start of each valid number
					while ymov > 0 and data[xmov][ymov-1].isdigit():
						ymov -= 1
					left_num_idxs.add((xmov,ymov))

	num_pile = deque(left_num_idxs)
	while num_pile:
		x, y = num_pile.popleft()
		res = ""
		while y < len(data[x]) and data[x][y].isdigit():
			res = res + data[x][y]
			y += 1
		part_numbers.append(int(res))

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

#209270 is wrong.  Not getting a high enough count.  Fak