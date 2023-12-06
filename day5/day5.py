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

def garden_search(seeds:list, mappings:dict, part:str):
	#Generates locations for each seed. 
	transfer_states = list(mappings.keys())
	if part == "A":
		lowpts = []
		for seed in seeds:
			lowpts.append(transformation_station(seed, mappings, transfer_states))
		return lowpts
	
	elif part == "B":
		transfers = list(mappings.keys())
		for transfer in transfers:
			order = "dest_start", "source_start", "range_length"
			ranges_to_test = [mappings[transfer][key] for key in order]
			ranges_to_test = list(zip(*ranges_to_test))
			seeds_dos = []
			while len(seeds) > 0:
				seedrange = seeds.pop()
				start, end = seedrange.start, seedrange.stop
				for dest, source, length in ranges_to_test:
					start_olap = max(start, source)
					end_olap = min(end, source + length)

					if start_olap < end_olap:
						seeds_dos.append(range(start_olap - source + dest, end_olap - source + dest))
						if start_olap > start:	
							seeds.append(range(start, start_olap))
						if end_olap < end:
							seeds.append(range(end_olap, end))
						break
				else:
					seeds_dos.append(range(start, end))
			seeds = seeds_dos
		
		lowpt = min(seed[0] for seed in seeds)
		return lowpt

@log_time
def part_A()->int:
	seeds, mappings = data_load("data")
	locations = garden_search(seeds, mappings, "A")
	return min(locations)

@log_time
def part_B()->int:
	seeds, mappings = data_load("test_data")
	seeds = [range(seeds[x], seeds[x] + seeds[x+1]-1) for x in range(0, len(seeds), 2)]
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

#Part B Notes
#So now the input seeds are actually ranges. 
#Making our seed posibility huge.  Meaning we can't use a list for 
#holding the low points because of the memory overflow. 
#Trick here was finding the overlapping ranges to tell whether or 
# not the boundaries of a range were even applicaable for a lowpoint
#If you go backwards through the seed list (hence the pop), you can find the 
#overlaps faster in the boundaries of the source/dest ranges. 
#That was hard as fuck. 