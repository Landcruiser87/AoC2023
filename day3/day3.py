import os
import sys
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from collections import deque
from utils.time_run import log_time
from utils.loc import recurse_dir
import numpy as np
DAY = './day3/'

def data_load(filen:str)->list:
	with open(f'{DAY}{filen}.txt', 'r') as f:
		data = f.read().splitlines()
		arr = [x.strip() if x != "" else "" for x in data]
	return arr

def engine_parts(data:list, part:str)->list:
	#gameplan
	#Iterate the grid. If any non alphanumerics found, iterate again in 1 square space.
	#If any numbers are found, Step left to the beginning of the number. 
	#Then step right to the end of the number. Add to a set as I could hit the same number twice 
	part_numbers = []
	for row, line in enumerate(data):
		for col, ch in enumerate(line):
			#If its a digit or period, move on and don't analyze it
			if (ch.isdigit()) | (ch == "."):
				continue

			#If its a nonalphanumeric.  Search nearby coordinates
			gear_numbers = set()
			res = ""
			for xmov in [row - 1, row, row + 1]:
				for ymov in [col - 1, col, col + 1]:
					# If we violate the grid shape and the number is not a digit, continue to the next mov
					if (xmov < 0) or (xmov >= len(data)) or (ymov < 0) or (ymov >= len(data[xmov])) or not data[xmov][ymov].isdigit():
						continue
					#Step left to find the start of each valid number
					while ymov > 0 and data[xmov][ymov-1].isdigit():
						ymov -= 1
					#Now step right until the end of the number
					while ymov < len(data[xmov]) and data[xmov][ymov].isdigit():
						res = res + data[xmov][ymov]
						ymov += 1
					gear_numbers.add(int(res))
					res = ""

			if part == "A":
				part_numbers.extend(list(gear_numbers))

			if part == "B" and len(gear_numbers) == 2:
				part_numbers.append(np.prod(list(gear_numbers)))
				
	return part_numbers

@log_time
def run_part_A():
	data = data_load("data")
	part_numbers = engine_parts(data, "A")
	return sum(part_numbers)

@log_time
def run_part_B():
	data = data_load("data")
	part_numbers = engine_parts(data, "B")
	return sum(part_numbers)
	
print(f"Part A solution: \n{run_part_A()}\n")
print(f"Part B solution: \n{run_part_B()}\n")
print(f"Lines of code \n{recurse_dir(DAY)}")

########################################################
#Notes
#Part A Notes

#strange puzzle input but we're looking at 
#engine schematics.  Any number that is seated next to an non-alphanumeric
#is a part number.  sum up all the part numbers. 
#need a function to return when a part number is adjacent to a symbol

#209270 is wrong.  Not getting a high enough count.  Fak
#I apparently can't loop over the nonalphanumeric indexes.  Need to stay in the main loop to avoid double entry

#Part B Notes. 
#Now, if any nonalphanumeric is sitting next to EXACTLY TWO numbers. 
#mutiply them together and add them to the part numbers list. 
#good god this needs a refactor.  Ugly as shit currently