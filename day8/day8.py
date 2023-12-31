import os
import sys
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utils.time_run import log_time
from utils.loc import recurse_dir
from collections import deque
from functools import reduce
from math import gcd
DAY = './day8/'

def data_load(filen:str)->list:
	with open(f'{DAY}{filen}.txt', 'r') as f:
		data = f.read().splitlines()
		arr = [x.strip() if x != "" else "" for x in data]
	return arr

def lcm(numbers):
    # Use the 'reduce' function to apply a lambda function that calculates the LCM for a pair of numbers.
    # The lambda function multiplies two numbers and divides the result by their greatest common divisor (gcd).
    # This process is applied cumulatively to all numbers in the list.
    return reduce((lambda x, y: int(x * y / gcd(x, y))), numbers)

def build_instructions(data):
	instructions = data[0]
	map_dict = {}
	for line in data[2:]:
		key, vals = line.split("=")
		key = key.strip()
		vals = (vals.strip(" ").replace("(", "").replace(")", ""))
		vals = tuple(vals.split(", "))
		map_dict[key] = vals

	return instructions, map_dict

def get_to_steppin(data:list, part:str):
	instructions, map_dict = build_instructions(data)
	if part == "A":
		steps = 0
		start = "AAA"
		end = "ZZZ"
		#I feel like he's trying to trick me 
		#with this while loop.....  ಠ_ಠ
		instruct = deque(list(instructions))

		while start != end:
			move = instruct.popleft()
			left = map_dict[start][0]
			right = map_dict[start][1]
			if move == "R":
				start = right
			else:
				start = left
			steps += 1
			if len(instruct) == 0: instruct.extend(list(instructions))
		return steps 
	
	if part == "B":
		starts = [key for key in map_dict.keys() if key.endswith("A")]
		route_table = len(starts) * [0]
		dir_dict = {"L":0, "R":1}
		for idx, route in enumerate(starts):
			#Set a deque (could use cycle) and popleft through vals
			dirs = deque(instructions)
			while not route.endswith("Z"):
				# increase the path of start positions
				route_table[idx] += 1
				#Grab the next route 
				next_idx = dirs.popleft()
				route = map_dict[route][dir_dict[next_idx]]
				if len(dirs) == 0: dirs.extend(list(instructions))
		#Use LCM to find the shortest path
		return lcm(route_table)

@log_time
def part_A():
	data = data_load("data")
	steps = get_to_steppin(data, "A")
	return steps

@log_time
def part_B():
	fail_list = [375488167]
	data = data_load("data")
	steps = get_to_steppin(data, "B")
	if steps in fail_list: raise ValueError("\nThat one doesn't work")
	return steps
	
print(f"Part A solution: \n{part_A()}\n")
print(f"Part B solution: \n{part_B()}\n")
print(f"Lines of code \n{recurse_dir(DAY)}")

########################################################
#Notes
#Part A Notes
#oooook.  Now we've got ghosts that we're lookign to avoid and need to do so by 
#using some maps the elves have to get out. 
#Main points. 
	#Going from AAA to ZZZ
	#first line is instructions of choosing the left or right tuple in a mapping
	#follow as such until you get to ZZZ.  
	#Repeat top line instruction until you get to ZZZ

#Part B Notes
# ehh now we are ghosts?  
# Goal is to track multiple paths at once.  Find the amount
# of steps will be the least common multiple of each value
# 375488167 -> Too low
