import os
import sys
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utils.time_run import log_time
from utils.loc import recurse_dir
import numpy as np

DAY = './day10/'
def data_load(filen:str)->list:
	with open(f'{DAY}{filen}.txt', 'r') as f:
		data = f.read().splitlines()
		arr = np.array([[str(x) for x in list(line)] for line in data], dtype=str)
	return arr

def onboard(data:np.array, x1:int, y1:int)->bool:
	ht = len(data)
	wd = len(data[0])
	if x1 < 0 or y1 < 0 or x1 >= ht or y1 >= wd:
		return False
	else:
		return True

def follow_the_paths(data:np.array)->int:
	row, col = np.where(data=="S")
	start = (row.item(), col.item())
	steps = 0
	positions = [start, start]
	
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
print(f"Part B solution: \n{part_B()}\n")
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