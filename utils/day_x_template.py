import os
import sys
from utils.time_run import log_time
from utils.loc import recurse_dir
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)


def data_load(filen:str)->list:
	# ./day/
	with open(f'./day1/{filen}.txt', 'r') as f:
		data = f.read().splitlines()
		arr = [x if x != "" else "" for x in data]
	return arr

@log_time
def run_part_A():
	data = data_load()


@log_time
def run_part_B():
	data = data_load()
	
print(f"Part A solution: \n{run_part_A()}\n")
print(f"Part B solution: \n{run_part_B()}\n")