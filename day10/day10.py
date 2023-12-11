import os
import sys
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utils.time_run import log_time
from utils.loc import recurse_dir
from itertools import chain

DAY = './day10/'
MOV_DICT = {
	"|":["N","S"],
	"-":["E","W"],
	"L":["N","E"],
	"J":["N","W"],
	"7":["S","W"],
	"F":["S","E"], 
	"S":["N","S","E","W"]
}
DIRS_DICT = {
	"N":(-1, 0),
	"S":(1, 0),
	"E":(0, 1),
	"W":(0, -1)
}
CON_DICT = {
	"N":"S",
	"S":"N",
	"E":"W",
	"W":"E"
}

def data_load(filen:str)->list:
	with open(f'{DAY}{filen}.txt', 'r') as f:
		data = f.read().splitlines()
		arr = [[str(x) for x in list(line)] for line in data]
	return arr

def onboard(data:list, x1:int, y1:int)->bool:
	ht = len(data)
	wd = len(data[0])
	if x1 < 0 or y1 < 0 or x1 >= ht or y1 >= wd:
		return False
	else:
		return True

def scan_neighbors(data:list, curr_p:tuple, next_p:tuple, direction:str):
	if onboard(data, next_p[0], next_p[1]) and data[next_p[0]][next_p[1]] != ".":
		next_val = MOV_DICT[data[next_p[0]][next_p[1]]]
		if len(set(CON_DICT[direction]) & set(next_val)) > 0:
			#Might need to check different combinations here. 
			return next_p
		#TODO - Need to rewrite this section to accomodate S starts

def follow_the_paths(data:list)->int:
	start = [[(row, col) for col in range(len(data[row])) if data[row][col]=="S"] for row in range(len(data))]
	start = tuple(chain(*start))[0]
	steps = [0, 0]
	start_walk = False
	visited = set([start])
	positions = [start, start]
	while True:
		for id, position in enumerate(positions):
			#Janky way to avoid first case where start/end match
			if positions[0] == positions[1] and not start_walk:
				start_walk = True
				end_walk = False
			
			for direction, (x, y) in DIRS_DICT.items():
				next_p = (position[0] + x, position[1] + y)
				if next_p not in visited:
					next_step = scan_neighbors(data, position, next_p, direction)
					if next_step:
						positions[id] = next_step
						visited.add(next_step)
						steps[id] += 1
						break #Need this break here to get out of the directional search. 

			if positions[0] == positions[1]:
				start_walk == False
				end_walk = True

		#To print the table after every 2 moves below
		sp = None
		for row in range(len(data)):
			for col in range(len(data[1])):
				if (row, col) == positions[0] or (row, col) == positions[1]:
					sp = "\033[1m" + data[row][col] + "\033[0m"
					col_id = col
			if sp:
				if col_id == 0:
					print(f"[*{sp}*, {str(data[row][col_id+1:])[1:]}")
				elif col_id == 4:
					print(f"{str(data[row][:col_id])[:-1]}, *{sp}*,")
				else:
					print(f"{str(data[row][:col_id])[:-1]}, *{sp}*, {str(data[row][col_id+1:])[1:]}")
				
				sp = None
			else:
				print(data[row][:])

		print("-"*30)
		# if positions[0] == positions[1]:
		# 	print("WINNA WINNA CHICKEN DINNA")
		# 	end_walk = True

	if steps[0] == steps[1]:
		return steps[0]
	
	#Intial path search, 
	#Then create two positions to track?

	print("fun")
@log_time
def part_A():
	data = data_load("test_data")
	steps = follow_the_paths(data)
	return steps
@log_time
def part_B():
	data = data_load("test_data")
	
print(f"Part A solution: \n{part_A()}\n")
# print(f"Part B solution: \n{part_B()}\n")
print(f"Lines of code \n{recurse_dir(DAY)}")

########################################################
#Notes
#Part A Notes

#Wow  So.  This is going to require a graph traversal at some point.  But!  we're chasing animals through 
#pipes now.  Super!  There are two main loops throughout the maze.  We need to discover how many
#steps it takes to get from start to finish.  
#Start is defined by S
#Finish is whe the two paths have the same end pt
#Use a dict for directions in the pipe. 
#Will need a way to scan a 1 grid border