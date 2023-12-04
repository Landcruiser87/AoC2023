import os
import sys
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utils.time_run import log_time
from utils.loc import recurse_dir

DAY = './day4/'
def data_load(filen:str)->list:
	with open(f'{DAY}{filen}.txt', 'r') as f:
		data = f.read().splitlines()
		arr = [x.strip() if x != "" else "" for x in data]
	return arr

def eval_cards(data:list, part:str):
	pts_list = []
	score_dict = {
		1:1, 2:2, 3:4, 4:8, 5:16,
		6:32, 7:64, 8:128, 9:256, 10:512
	}
	if part == "B":
		card_dict = {card_num.split(":")[0].split()[0] + " " + card_num.split(":")[0].split()[1]:1 for card_num in data}

	for card in data:
		card_num, nums = card.split(":")
		winning, drawn = nums.split("|")
		#Find intersection of winning and drawn with sets
		wins = set(winning.split()) & set(drawn.split())
		if len(wins) > 0:
			pts_list.append(score_dict[len(wins)])

		if part == "B":
			_, car_id = card_num.split()
			#Get the current count at this round of how many cards you have
			curr_count = card_dict[f"Card {int(car_id)}"]
			#Iterate thruogh the current card counts to yield card win rewards
			#The plus 1 is for the intial card in each round
			while curr_count > 0:
				for car in range(len(wins)):
					card_dict[f"Card {int(car_id) + car + 1}"] += 1
				curr_count -= 1

	if part == "A":
		return pts_list
	
	elif part == "B":
		stack_count = list(card_dict.values())
		return stack_count
	
@log_time
def run_part_A():
	data = data_load("data")
	winning_cards = eval_cards(data, "A")
	return sum(winning_cards)

@log_time
def run_part_B():
	data = data_load("data")
	winning_cards = eval_cards(data, "B")
	return sum(winning_cards)
	
print(f"Part A solution: \n{run_part_A()}\n")
print(f"Part B solution: \n{run_part_B()}\n")
print(f"Lines of code \n{recurse_dir(DAY)}")

########################################################
#Notes
#Scratchcards

#Part A Notes
#It looks we have a bunch of cards that have two sets of numbers
#In each line
#left of the pipe - winning numbers
#right of the pipe - numbers drawn
#one match = one point.
#any match after in one line doubles the points
#calculate total 

#gameplan
#Set intersection 