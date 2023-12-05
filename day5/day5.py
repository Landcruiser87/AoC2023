import os
import sys
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utils.time_run import log_time
from utils.loc import recurse_dir
from collections import deque
from itertools import chain
DAY = './day5/'
def append_dict(dict_obj:dict, key:str, title:str, val:list):
	"""Appends a value to a dictionary.  If the key already exists, it appends the value to the list.

	Args:
		dict_obj (dict): Dictionary to attach things too
		key (str): Key of the dict
		val (list): List of items to add
	"""	
	try:
		dict_obj[title][key].append(val)
	except KeyError:
		dict_obj[title][key] = [val]
	#map format
	#source range start | dest range start | range length 
	#dict structure
	#maptitle
		#source range start | dest range start | range length | dest_vals | source_vals

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
				append_dict(mappings, "dest_start", title, maps[0])
				append_dict(mappings, "source_start", title, maps[1])
				append_dict(mappings, "range_length", title, maps[2])
				append_dict(mappings, "dest_vals", title, range(maps[0], maps[0] + maps[2]))
				append_dict(mappings, "source_vals", title, range(maps[1], maps[1] + maps[2]))
	return seeds, mappings

def transformation_station(seed:int, mappings:dict, actions:list)->int:
	trans_val = [seed]
	for action in actions:
		s_ranges = list(mappings[action]["source_vals"])
		found = False
		for idx, s_range in enumerate(s_ranges):
			if trans_val[-1] in s_range and not found:
				#Need a way to index.... source vals, enumerate? ahhhh.  index the src list of the seed.  Use that index in the dest_vals!!
				src_idx = mappings[action]["source_vals"][idx].index(trans_val[-1])
				trans_val.append(mappings[action]["dest_vals"][idx][src_idx])
				found = True			
		if not found:
			trans_val.append(trans_val[-1])
	return trans_val[-1]
	
def garden_search(seeds:str, mappings:dict, part:str)->int:
	#Generates locations for each seed. 
	lowpts = []
	transfer_states = list(mappings.keys())
	if part == "A":
		for seed in seeds:
			lowpts.append(transformation_station(seed, mappings, transfer_states))
		return lowpts
	elif part == "B":
		lowpt = 10_000_000_000
		for seedrange in seeds:
			for seed in (seedrange[0], seedrange[-1]):
				low = transformation_station(seed, mappings, transfer_states)
				if low < lowpt:
					lowpt = low
		return lowpt

@log_time
def part_A():
	seeds, mappings = data_load("data")
	locations = garden_search(seeds, mappings, "A")
	return min(locations)

@log_time
def part_B():
	seeds, mappings = data_load("data")
	seeds = [range(seeds[x], seeds[x] + seeds[x+1]) for x in range(0, len(seeds), 2)]
	location = garden_search(seeds, mappings, "B")
	return location

	
print(f"Part A solution: \n{part_A()}\n")
print(f"Part B solution: \n{part_B()}\n")
print(f"Lines of code \n{recurse_dir(DAY)}")

########################################################
#Notes 
#Part A Notes
#Well this is a weird one. 
#Our job is to find the lowest location of where to plant but we have to transform from a seed locatino through
#various mappings to get the right location.
#Probably use a dictionary of dicts for the mappings
  
