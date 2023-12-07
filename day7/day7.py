import os
import sys
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utils.time_run import log_time
from utils.loc import recurse_dir
from collections import Counter

DAY = './day7/'
CARD_ORDER = {
	2:0, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7,
	"T":8,"J":9,"Q":10, "K":11, "A":12
}
HAND_ORDER = {
	0:"high_card",
	1:"one_pair",
	2:"two_pair",
	3:"threeofakind",
	4:"fullhouse",
	5:"fourofakind",
	6:"fiveofakind"
}
def data_load(filen:str)->list:
	with open(f'{DAY}{filen}.txt', 'r') as f:
		data = f.read().splitlines()
		arr = [tuple(x.split()) if x != "" else "" for x in data]
		arr = [(x[0],int(x[1])) for x in arr]
	return arr

def resolve_tie():
	pass

def calc_hand():
	pass

def pokertown(data:list, part:str):
	for hand, bid in data:
		counts = Counter(hand)
		if any(x>=4 for x in counts.values()):
			pass
	#1. Decide order by HAND_ORDER
	#2. Resolve Ties
	#3. Multiply bid by its rank

@log_time
def part_A():
	data = data_load("test_data")
	totalwinnings = pokertown(data, "A")
	return sum(totalwinnings)

@log_time
def part_B():
	data = data_load()
	totalwinnings = pokertown(data)
	return sum(totalwinnings)
	
print(f"Part A solution: \n{part_A()}\n")
# print(f"Part B solution: \n{part_B()}\n")
print(f"Lines of code \n{recurse_dir(DAY)}")

########################################################
#Notes
#Part A Notes
#So we're playing some poker!  Camel poker that is.  Our jobs here is to calculate the total 
#winnings of each game. To start we'll take all the hands and 
#order them by strength.  Standard poker levels apply here but the tie resolution is different. 
#in a tie, we go by each individual charater from the left and see whats higher. Once the order is 
#figured, we just need to multiply the rank by the bid (int to the right of the hand)
#and then add up all our winnings.   OK!
