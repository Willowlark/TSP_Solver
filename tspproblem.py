from math import sqrt
from sys import maxint
import copy
import time
cache = {}

""" 
This program solves a traveling salesman problem. It takes tsp 
files as input. Further details on each sections.
Author: Bill Clark (Unless otherwise noted)
"""

#Global vars.
citycount = 0
cities = {}
shortestdistance = maxint
shortestpermuation = []
start = 0

#Permuation function by by John.
#uses a python generator to cycle through permuations.
def combi(xs, low=0):
	if low + 1 >= len(xs):
            yield xs
	else:
		for p in combi(xs, low + 1):
			yield p        
		for i in range(low + 1, len(xs)):
			xs[low], xs[i] = xs[i], xs[low]
			for p in combi(xs, low + 1):
				yield p
			xs[low], xs[i] = xs[i], xs[low]

#Does the distance formula on two lists of an ordered pair.	
def distance_math(one, two):
	x = sqrt((two[0] - one[0])**2 + (two[1] - one[1])**2)
	return x

#Asks for a file, then reads in the relevant information.
f = raw_input("enter filename: ")
start = time.time()

file = open(f, 'r')
for line in file:
	words = line.split()
	if words[0] == 'DIMENSION:':
		citycount = int(words[1])
	if words[0].isdigit():
		x = [int(float(words[1])), int(float(words[2]))]
		cities[int(words[0])] = x
	else:
		pass
#Main operation loop. uses two for loops, one for the possible permuations,
#the second cycles through the permutation and does the distance formula.
for p in combi([x+1 for x in range(citycount)]):
	trip_distance = 0
	for i in range(0, len(p)):
		'''This is your suggested addition, the cache functionality.
		While it seemed like it would work faster, the distance_math
		only calls one function, while the x in s function of the below
		if statment is O(n). so while the code for getting things from 
		a dictionary is O(1), the extra O(n) gave us an extra 6 seconds
		on a mini2, which will continue to impact the code from there.
		We felt it was best to keep it out. 	
		'''
		#if [ p[i], p[(i+1)%len(p)] ] in cache.keys():
		#	distance = cache[ p[i], p[(i+1)%(len(p))] ]
		#else:
		#	distance = distance_math(cities[p[i]], cities[p[(i+1)%len(p)]])
		#	cache[ p[i], p[(i+1)%(len(p))] ] = distance
		distance = distance_math(cities[p[i]], cities[p[(i+1)%len(p)]])
		trip_distance = trip_distance + distance
	if trip_distance < shortestdistance:
		shortestdistance = trip_distance
		shortestpermuation = copy.deepcopy(p)

#Prints out best solution.		
print shortestpermuation, 'shortest order.'
print shortestdistance, 'shortest time.'
print 'program ends: ' + repr(time.time()-start)
