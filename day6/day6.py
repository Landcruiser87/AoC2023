import os
import sys
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utils.time_run import log_time
from utils.loc import recurse_dir
import numpy as np


DAY = './day6/'
def data_load(filen:str)->list:
	with open(f'{DAY}{filen}.txt', 'r') as f:
		data = f.read().splitlines()
		arr = [x.strip() if x != "" else "" for x in data]
	return arr

def calc_win_times(data:list, part:str):
	racewins, wins = 0, []
	if part == "A":
		times = [int(x) for x in data[0].split(":")[1].strip().split()]
		distances = [int(x) for x in data[1].split(":")[1].strip().split()]
		for race_time in times:
			for holdtime in range(1, race_time - 1):
				rate = race_time - holdtime
				distancetraveled = holdtime * rate
				if distancetraveled > distances[times.index(race_time)] :
					racewins += 1
			wins.append(racewins)
			racewins = 0

	elif part == "B":
		time = int("".join([x for x in data[0].split(":")[1].strip() if x.isdigit()]))
		distance = int("".join([x for x in data[1].split(":")[1].strip() if x.isdigit()]))
		for holdtime in range(1, time - 1):
			rate = time - holdtime
			distancetraveled = holdtime * rate
			if distancetraveled > distance:
				racewins += 1
		wins.append(racewins)
		racewins = 0
	
	return wins

@log_time
def part_A():
	data = data_load("data")
	winningtimes = calc_win_times(data, "A")
	return np.prod(winningtimes)

@log_time
def part_B():
	data = data_load("data")
	winningtimes = calc_win_times(data, "B")
	return np.prod(winningtimes)
	
print(f"Part A solution: \n{part_A()}\n")
print(f"Part B solution: \n{part_B()}\n")
print(f"Lines of code \n{recurse_dir(DAY)}")

########################################################
#Notes
#Part A Notes
#Its a boat race!  We have toy boats with buttons on top.  
#The boat won't move unless you hold down the button, and the boat won't move 
#if you don't release the button.  
#They key thing to remember is 
	#!for one second of button hold, the speed increases by one second

