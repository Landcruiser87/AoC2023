import os
import sys
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utils.time_run import log_time
from utils.loc import recurse_dir
import numpy as np

DAY = './day2/'
CUBE_MAX = {
	"red":12,
	"green":13,
	"blue":14,
}

def data_load(filen:str)->list:
	with open(f'{DAY}{filen}.txt', 'r') as f:
		data = f.read().splitlines()
		arr = [x.split(":") if x != "" else "" for x in data]
	return arr

def gleamingthecube(data:list, part:str)->list:
	valid_games = []
	for game in data:
		cube_d = {
			"red":0,
			"green":0,
			"blue":0,
		}
		rolls = game[1].split(";")
		for roll in rolls:
			roll = roll.split(",")
			for cube in roll:
				cube = cube.strip()
				count, color = cube.split(" ")
				if cube_d[color] < int(count):
					cube_d[color] = int(count)
		if part == "A":
			counter = 0
			for color in CUBE_MAX.keys():
				if cube_d[color] <= CUBE_MAX[color]:
					counter += 1
				if counter == 3:
					valid_games.append(game[0])
		else:
			valid_games.append(list(cube_d.values()))
	if part == "A":
		ids = [int(gam.split(" ")[1]) for gam in valid_games]
		return ids
	else:
		powers = [np.prod(gam) for gam in valid_games]
		return powers

@log_time
def run_part_A():
	data = data_load("data")
	game_ids = gleamingthecube(data, "A")
	return sum(game_ids)

@log_time
def run_part_B():
	data = data_load("data")
	game_ids = gleamingthecube(data, "B")
	return sum(game_ids)
	
print(f"Part A solution: \n{run_part_A()}\n")
print(f"Part B solution: \n{run_part_B()}\n")
print(f"Lines of code \n{recurse_dir(DAY)}")

########################################################
#Notes
#Part A Notes
#Goal
#Sum the game indices that are valid. 
#Or job is to invalidate games that don't
#So we want the possible color counts to the
#the max of whatever we see pulled out in each turn of the 1 round. 

#Part B Notes
#this time we multiply the max counts of each bag and return that instead