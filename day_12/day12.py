import os
import sys
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utils.time_run import log_time
from utils.loc import recurse_dir
from itertools import combinations

DAY = '../day_12/'
def data_load(filen:str)->list:
	with open(f'{DAY}{filen}.txt', 'r') as f:
		data = f.read().splitlines()
		arr = [x.strip() if x != "" else "" for x in data]
	return arr

def find(line:str, ch:int):
	return [x for x, ltr in enumerate(line) if ltr == ch]


def decode_springs(data:list, part:str):
	'''
	. -> operational
	# -> broken
	? -> unknown
	'''
	counts = []
	for springs in data:
		line, groups = springs.split(" ")
		groups = list(map(int, groups.split(",")))
		
		unknown = find(line, "?")
		broken = find(line, "#")
		functional = find(line, ".")
		total_unassign_springs = sum(groups) - len(broken)
		
		for combo in combinations(unknown, total_unassign_springs):
			print(combo)

	return counts


@log_time
def part_A():
	data = data_load("test_data")
	counts = decode_springs(data, "A")
	return counts

@log_time
def part_B():
	data = data_load()
	
print(f"Part A solution: \n{part_A()}\n")
# print(f"Part B solution: \n{part_B()}\n")
print(f"Lines of code \n{recurse_dir(DAY)}")

########################################################
#Notes
#Part A Notes
#now we're dealing with broken springs and we need to find the ones that work
#Our input is split.  Each line is a group of springs.  The data is split such
#that every row as one map and to the right, are the group counts of broken
# springs Our job is to count the possible number of combinations of groups that
#could exist in each springmap (row).  