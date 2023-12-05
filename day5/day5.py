import os
import sys
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utils.time_run import log_time
from utils.loc import recurse_dir

DAY = './day5/'
def data_load(filen:str)->list:
	with open(f'{DAY}{filen}.txt', 'r') as f:
		data = f.read().splitlines()
		seeds = data[0][7:].split()
		seeds = [int(x) for x in seeds]
		arr = [x.strip() if x != "" else "" for x in data[2:]]
		mappings = {}
		for mapping in arr:
			if "-" in mapping:
				title = mapping[:-5]
				mappings[title] = dict()
			elif any(x.isdigit() for x in mapping):
				maps = mapping.split()
				maps = [int(x) for x in maps]
				mappings[title]["dest_start"] = maps[0]
				mappings[title]["source_start"] = maps[1]
				mappings[title]["range_length"] = maps[2]
			
	return seeds, mappings

def garden_search(seeds:str, mappings:dict):
	pass

@log_time
def part_A():
	seeds, mappings = data_load("test_data")
	locations = garden_search(seeds, mappings)
	return min(locations)

@log_time
def part_B():
	data = data_load()
	
print(f"Part A solution: \n{part_A()}\n")
# print(f"Part B solution: \n{part_B()}\n")
print(f"Lines of code \n{recurse_dir(DAY)}")

########################################################
#Notes 
#Part A Notes
#Well this is a weird one. 
#Our job is to find the lowest location of where to plant but we have to transform from a seed locatino through
#various mappings to get the right location.
#Probably use a dictionary of dicts for the mappings
  
