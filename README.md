### Generate Teams for CS 342

A Python program that allows for easy team and topic assigment for groups. 

Input:  
One text file with each line containing the netids of all enrolled students, another text file in which each lines contains desired pairings and ranked preferences.

Output:   
A text file with each line containing the assigned team and the topic. 


This program does not attempt to force topics on any particular group to try and balance the number of groups doing particular topics. While this could be done in a fair way using randomization, there currently isn't a constraint on the number of groups that can do a topic, so the decision was made to instead simply follow student preferences.  
The primary function of the program is to agglomerate preferences from the input individuals or pairs and get "composite" preferences for the whole group. This has to be done in a fair manner.

1. Fair: Each person's preferences are considered when choosing the topic for each group. This occurs even if a pair of people with the same preferences were matched to a single person to form a group of three; the single person's preferences are weighed the same as the pair's preferences for choosing the group's topic. This ensures the individual still gets a say and is not simply out-voted. 
2. Equitable: All students are considered for their preferences (there is no group, random or determined, that is not considered for their preferences.) The individual is not out-weighed by the pair they are matched with. 
3. Explainable: The program uses simple topic similarity to match pairs with other pairs as well as individuals with other individuals, and then chooses a topic by using both frequency of preference and ranking of preference for topics in the group's "composite preference".