import os
import sys
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utils.time_run import log_time
from utils.loc import recurse_dir
from collections import Counter

DAY = './day7/'
global CARD_ORDER
CARD_ORDER = {
	"2":0, "3":1, "4":2, "5":3, "6":4, "7":5, "8":6, "9":7,
	"T":8,"J":9,"Q":10, "K":11, "A":12
}
HAND_ORDER = {
	0:"highcard",
	1:"onepair",
	2:"twopair",
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

def swap_jokers():
	global CARD_ORDER
	CARD_ORDER = {
		"2":1, "3":2, "4":3, "5":4, "6":5, "7":6, "8":7, "9":8,
		"T":9,"J":0,"Q":10, "K":11, "A":12
	}

def score_hands(data:list, part:str):
	order = []
	for hand, _ in data:
		counts = list(Counter(hand).values())
		if part == "B":
			if "J" in hand:
				counts = joker_upgrade(hand, counts)
		if 5 in counts:
			hand_strength = (hand, HAND_ORDER[6], 6)
		elif 4 in counts:
			hand_strength = (hand, HAND_ORDER[5], 5)
		elif 3 in counts:
			if 2 in counts:
				hand_strength = (hand, HAND_ORDER[4], 4)
			else:
				hand_strength = (hand, HAND_ORDER[3], 3)
		elif 2 in counts:
			twop = 0
			for count in counts:
				if count==2:
					twop += 1
			if twop > 1:
				hand_strength = (hand, HAND_ORDER[2], 2)
			else:
				hand_strength = (hand, HAND_ORDER[1], 1)
		else:
			hand_strength = (hand, HAND_ORDER[0], 0)
		order.append(hand_strength)
	order.sort(key=lambda x:x[2], reverse=True)
	return order, {k:v for k, v in data}

def joker_upgrade(hand:str, counts:dict):
	j_howmany = hand.count("J")
	#Catch one edge case for all J's.  
	if j_howmany == 5:
		return [5]
	
	#5 of a kind case
	elif 4 in counts and j_howmany == 1:
		idx = counts.index(4)
		counts[idx] += 1

	#4 of a kind case
	elif 3 in counts and j_howmany <= 2:
		#3 of some kind with 2 J's
		idx = counts.index(3)
		if j_howmany <= 2:
			#have 3 of some kind with 2 J's
				#Boosts to 5 of a kind
			#have 3 of some other kind with 1 J
				#Boosts to 4 of a kind
			counts[idx] += j_howmany
		elif j_howmany == 3:
			#Rare case but I have 3 J's that now boost the other 2 count to
				#Boosts to 5 of a kind
			if 2 in counts:
				counts[counts.index(2)] += j_howmany
				#Happens twice

	elif 2 in counts and j_howmany <= 3:
		idx = counts.index(2)
		if j_howmany <= 2 and counts.count(2) == 1:
			counts[idx] += 1
		else:
			counts[idx] += j_howmany	

	elif 1 in counts:
		idx = counts.index(1)
		counts[idx] += j_howmany

	return counts

def resolve_ties(hands:list):
	#Get the counts of the hands
	counts = Counter(x[1] for x in hands)
	rev_map = {v:k for k, v in CARD_ORDER.items()}
	hand_list = [x[0] for x in hands]
	#Had to keep the set calcs to make sure the order stayed the same.
	hand_types = sorted((set([(x[1],x[2]) for x in hands])), key=lambda y:y[1], reverse=True)
	hand_types = [x[0] for x in hand_types]

	for handtype in hand_types:
		if counts[handtype] >= 1:
			# If you find any ties, find the winner
			ties = [x[0] for x in hands if x[1]==handtype]
			tie_index = [hand_list.index(x[0]) for x in hands if x[1]==handtype]
			#Map all the characters to their values
			ties_map = [[CARD_ORDER[ch] for ch in lilhand] for lilhand in ties]
			#sort the list by all columns and reverse them
			orderzip = sorted(ties_map, key=lambda x:x[:], reverse=True)
			map_order = ["".join([rev_map[ch] for ch in lilhand]) for lilhand in orderzip]
			for idx in tie_index:
				hand_list[idx] = map_order.pop(0)

	return hand_list[::-1]

def calc_wins(ordered:list, bid_dict):
	score = []
	for idx, handid in enumerate(ordered):
		score.append(bid_dict[handid]*(idx+1))
	return score

def pokertown(data:list, part:str):
	#1. Calculate hand strengths
	#2. Decide order by HAND_ORDER
	#3. Resolve Ties
	#4. Multiply bid by its rank

	if part == "B":
		swap_jokers()
	hand_st, bid_dict = score_hands(data, part)
	ordered = resolve_ties(hand_st)
	totalwinnings = calc_wins(ordered, bid_dict)
	return totalwinnings

@log_time
def part_A():
	data = data_load("data")
	totalwinnings = pokertown(data, "A")
	return sum(totalwinnings)

@log_time
def part_B():
	data = data_load("data")
	totalwinnings = pokertown(data, "B")
	return sum(totalwinnings)
	
print(f"Part A solution: \n{part_A()}\n")
print(f"Part B solution: \n{part_B()}\n")
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

#Nopes
#255934144
#253787668
#254864651
#253566764
#255710028
#254281054  
#247869019

#Part B Notes. 
#ooook.  Now jacks are jokers and have a weight value of 0. Jokers are also wild
#for increasing hand strength.  Will need a separate function to adjust the 
#counts. Rest of the code should behave accordingly with the new
#weight

#Nopes
# 245908369 -> too high
# 245557617 -> too high
# 245893562 -> too high
# 245557617