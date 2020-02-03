"""
https://docs.google.com/document/d/1Z0HUoaegVDAxj4fr7Np3mR7-Yox-Gw-dDYWhnLQjkAA/edit

A python program that will create groups for an assignment which will be done in groups of four.  

Input: List of students, list of desired pairings, and ranked preferences.

Output: Groups of 3, 4, or 5, preferred 4,      	
ola, rcd, ksm, 3

Use randomness to ensure a fair process. 
Everyone should get at least one of the topics that they signed up for, but this is not guaranteed. 

Steps 
1. Assign groups. Assign desired pairs to each other, and others in a random group. 
"""
import re
import random 
from collections import defaultdict
from difflib import SequenceMatcher



def process_inputs(netids, prefs):
	# Randomly assign order to netids
	random.shuffle(netids)
	netid_to_num = {netid: i for i, netid in enumerate(netids)}

	data = []
	for pref in prefs:
		new_pref = re.split('\W+', pref)
		data.append(new_pref)
	
	topic_pref_map = {}
	for line in data: 
		topic_pref_map[line[0]] = ''.join(line[-3:])	
	
	pairs = set()
	singles = set()
	for line in data:
		if len(line) > 4:
			pair = ' '.join(sorted([line[0], line[1]]))
			pairs.add(pair)
		else: 
			singles.add(line[0])
	
	# Assign topic preference to the team
	for pair in pairs: 
		topic_pref_map[pair] = topic_pref_map[pair.split()[0]]

	# print topic_pref_map

	# print (pairs, singles)
	# return data, netid_to_num

	final_teams = {}
	teams = pairs.union(singles)
	finished = []	
	for team in teams:
		if team in finished: 
			continue 
		other_teams = [t for t in teams if t != team]
		team_pref = topic_pref_map[team]
		similarity_dict = {t: similar(topic_pref_map[t], team_pref)
							for t in other_teams}		
		closest_team = max(similarity_dict, key=similarity_dict.get)
		closest_team_pref = topic_pref_map[closest_team]

		new_team = ' '.join([team, closest_team])
		new_team_prefs = ''.join([team_pref, closest_team_pref])
		final_teams[new_team] = new_team_prefs
		finished.extend([team, closest_team])

	result = []
	for team, team_prefs in final_teams.items():
		team = ', '.join(team.split())
		result.append("{}, {}".format(team, assign_topic(team_prefs)))
	
	return result

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def assign_topic(group_topic):
	# Return the top-most topic that is liked by both subgroups in the group.
	seen = []
	for topic in group_topic:
		if topic not in seen:
			seen.append(topic)
		else: 
			return topic
	return seen[0]



if __name__ == '__main__':
	prefs = ['ola, rcd, 1, 5, 3', 'rcd, ola, 1, 5, 3','ksm 3, 7, 1']
	netids = ['ola', 'ksm', 'rcd']
	print (process_inputs(netids, prefs))
