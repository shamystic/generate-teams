"""
https://docs.google.com/document/d/1Z0HUoaegVDAxj4fr7Np3mR7-Yox-Gw-dDYWhnLQjkAA/edit

A python program that will create groups for an assignment which will be done in groups of four.  

Input: List of students, list of desired pairings, and ranked preferences.

Output: groups.txt file of 3, 4, or 5, preferred 4, members with a topic:
ola, rcd, ksm, 3.
"""
import re
import random 
from collections import defaultdict
from difflib import SequenceMatcher
from collections import Counter


def process_inputs(netid_filename, prefs_filename) -> (list(), list()):
	# Read in data.
	netid_file = open(netid_filename, 'r')
	netids =  netid_file.read().splitlines()
	netid_file.close()

	prefs_file = open(prefs_filename, 'r')
	prefs =  prefs_file.read().splitlines()
	prefs_file.close()
	return netids, prefs

def generate_teams(netids, prefs) -> list():

	# Process input data
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
		try: 
			topic_pref_map[pair] = topic_pref_map[pair.split()[0]] + \
							   topic_pref_map[pair.split()[1]]
		except KeyError: 
			topic_pref_map[pair] = topic_pref_map[pair.split()[0]]


	# Use similarity matching to put the people who did not request pairs into a pair with someone with similar interests. 
	finished = []
	for single in singles: 
		if single in finished: 
			continue 
		other_singles = list(set([s for s in singles if s != single])\
						   .difference(set(finished)))
		single_pref = topic_pref_map[single]
		similarity_dict = {s: similar(topic_pref_map[s], single_pref)
							for s in other_singles}
		try:
			closest_person = max(similarity_dict, key=similarity_dict.get)
			closest_person_pref = topic_pref_map[closest_person]

			new_pair = ' '.join([single, closest_person])
			new_pair_prefs = ''.join([single_pref, closest_person_pref])
			pairs.add(new_pair)
			topic_pref_map[new_pair] = new_pair_prefs
			finished.extend([single, closest_person])
		# No person to match with :(
		except ValueError:
			continue

	for person in finished:
		singles.discard(person)

	final_teams = {}
	teams = pairs.union(singles)
	finished = []
	finished_netids = []
	for team in teams:
		if team in finished: 
			continue 
		other_teams = list(set([t for t in teams if t != team])\
						   .difference(set(finished)))
		team_pref = topic_pref_map[team]
		similarity_dict = {t: similar(topic_pref_map[t], team_pref)
							for t in other_teams}		
		closest_team = max(similarity_dict, key=similarity_dict.get)
		closest_team_pref = topic_pref_map[closest_team]

		new_team = ' '.join([team, closest_team])
		new_team_prefs = ''.join([team_pref, closest_team_pref])
		final_teams[new_team] = new_team_prefs
		finished.extend([team, closest_team])
		finished_netids.extend(team.split() + closest_team.split())

	# Generate output. 
	result = []
	for team, team_prefs in final_teams.items():
		team = ', '.join(team.split())
		result.append("{}, {}".format(team, assign_topic(team_prefs)))
	
	# Sort by group size to add any stragglers who did not submit the google form.
	result = sorted(result, key=len)
	leftover_students = list(set(netids) - set(finished_netids))
	print('The following students failed to submit the category selection form:', leftover_students)
	# Add the stragglers to the smallest teams. 
	curr_team = 0
	for i in range(len(leftover_students)):
		result[curr_team] = leftover_students[i] + ', ' + result[curr_team]
		if curr_team + 1 < len(result):
			curr_team += 1

	return result

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def assign_topic(group_topic):
	# Return the top-most topic that is liked by the most subgroups in the group.
	group_topic = list(group_topic)
	most_common = Counter(group_topic).most_common(1)[0][0]
	top_topics = Counter(group_topic).most_common(3)
	topic_vals = [a[0] for a in Counter(group_topic).most_common(3)]	
	if top_topics[0][1] == top_topics[1][1]:
		# Need to break ties
		prefs_chunks = list(chunks(group_topic, 3))
		index_sums = {}
		for i in range(len(group_topic)):
			topic = group_topic[i]
			index_sums[group_topic[i]] = sum([chunk.index(topic) if topic in chunk else 0 for chunk in prefs_chunks])			 		
		return min(topic_vals, key=index_sums.get)
	else: 
		return most_common


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Fair because it does not prioritize group over the individual


if __name__ == '__main__':

	netids, prefs = process_inputs('students.txt', 'preferences.txt')
	result = generate_teams(netids, prefs)
	out = open('teams.txt', 'w+')
	out.writelines(result)
	print('Generated teams file teams.txt.')