import os
import sys
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utils.time_run import log_time
from utils.loc import recurse_dir
from collections import Counter, deque

DAY = './day7/'
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

def score_hands(data:list):
	order = []
	for hand, _ in data:
		counts = Counter(hand)
		#Use a Counter to calulate raw hand strengths.  Will resolve ties next
		if any(x>4 for x in counts.values()):
			hand_strength = (hand, HAND_ORDER[6], 6)
		elif any(x==4 for x in counts.values()):
			hand_strength = (hand, HAND_ORDER[5], 5)
		elif any((x==3) for x in counts.values()):
			if any((x==2) for x in counts.values()):
				hand_strength = (hand, HAND_ORDER[4], 4)
			else:
				hand_strength = (hand, HAND_ORDER[3], 3)

		elif any(x==2 for x in counts.values()):
			twop = 0
			for count in counts.values():
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

def resolve_ties(hands:list):
	#Get the counts of the hands
	counts = Counter(x[1] for x in hands)
	rev_map = {v:k for k, v in CARD_ORDER.items()}
	hand_list = [x[0] for x in hands]
	#Had to keep the set calcs to make sure the order stayed the same.  I could take the keys of the counts
	#But there was no guarantee the order would remain.  This way ensures it. 
	hand_types = sorted((set([(x[1],x[2]) for x in hands])), key=lambda y:y[1], reverse=True)
	hand_types = [x[0] for x in hand_types]

	for handtype in hand_types:
		if counts[handtype] >= 2:
			# If you find any ties, find the winner
			ties = [x[0] for x in hands if x[1]==handtype]
			#Map all the characters to their values
			ties_map = [[CARD_ORDER[ch] for ch in lilhand] for lilhand in ties]
			#sort the list by all columns and reverse them
			orderzip = sorted(ties_map, key=lambda x:x[:], reverse=True)
			map_order = ["".join([rev_map[ch] for ch in lilhand]) for lilhand in orderzip]

			#Get indexes of current map orders
			#Assign them to a temp switch dict. 
			#Swich them vals. 
			old_idx = deque([hand_list.index(x) for x in map_order])
			if ties != map_order:			 
				while old_idx:
					old_id = old_idx.popleft()
					new_id = old_idx.popleft()
					hands = swap_places(hands, old_id, new_id)

	return hands[::-1]

def swap_places(src_list:list, i:int, j:int)->list:
	elem_i = src_list[i]
	elem_j = src_list[j]
	src_list[i] = elem_j
	src_list[j] = elem_i
	return src_list

def calc_wins(ordered:list, bid_dict):
	score = []
	for idx, (handid, _, _) in enumerate(ordered):
		score.append(bid_dict[handid]*(idx+1))
	return score

def pokertown(data:list, part:str):
	#1. Calculate hand strengths
	#2. Decide order by HAND_ORDER
	#3. Resolve Ties
	#4. Multiply bid by its rank

	hand_st, bid_dict = score_hands(data)		
	ordered = resolve_ties(hand_st)
	totalwinnings = calc_wins(ordered, bid_dict)
	return totalwinnings

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

#Nopes
#255934144
#253787668
#254864651
#253566764
#255710028
#254281054  

#Fun trick for remapping the values to compare each character in a list of tuples
# zip_ties = list(zip(*ties_map))
# #Make a pile of tuples to compare
# zip_deq = deque(zip_ties)
# idx = 0
# while the length of the set comparisons is equal to 1. 
#I used a set because there may be a 3way or more tie and i need to extend it 
#throughout the entire list
# while True:
# 	#move from the bottom of the list and check each
# 	#first character to see who's greater or if there's a match.
# 	temp = zip_deq.popleft()
# 	if len(set(temp))==1:
# 		#Track the idx as we move through the pile
# 		idx += 1
# 		continue
# 	else:
		#Map the values back to characters for indexing