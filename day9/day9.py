import os
import sys
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utils.time_run import log_time
from utils.loc import recurse_dir
import numpy as np

DAY = './day9/'
def data_load(filen:str)->list:
	with open(f'{DAY}{filen}.txt', 'r') as f:
		data = f.read().splitlines()
		arr = [x.strip() if x != "" else "" for x in data]
	return arr
def predict_next(line, temp)->int:
	pass

def extrapolate(data:list)->list:
	predictions, depth = [], 0
	for line in data:
		temp = [int(num) for num in line.split()]
		while True:
			diff = np.diff(temp)
			depth += 1
			if np.all(diff==0) and len(diff) > 1:
				predictions.append(predict_next(line, temp))
				depth = 0
				break
			else:
				temp = diff
	return predictions

@log_time
def part_A():
	data = data_load("test_data")
	predictions = extrapolate(data)
	return sum(predictions)

@log_time
def part_B():
	data = data_load()
	
print(f"Part A solution: \n{part_A()}\n")
print(f"Part B solution: \n{part_B()}\n")
print(f"Lines of code \n{recurse_dir(DAY)}")

########################################################
#Notes
#Part A Notes
#Neat problem setup.  So, we take the difference of each value in the input
#until all values == 0.  At that point, we want to predict the next value
#in the input sequence.  We do so by ensureing the diffs above it all equal
#zero  i think ... i can just reverse that process