from math import sqrt
from sys import maxint
import copy
import time

#Global variables.
citycount = 0
cities = {}
shortestdistance = maxint
shortestpath = []
start = 0

#Calculates the distance between two cities, stored as an
#ordered pair list.
def distance_math(one, two):
	x = sqrt((two[0] - one[0])**2 + (two[1] - one[1])**2)
	return x

#Asks for a file, then reads in the relevant information.
f = raw_input("enter filename: ")

#starts the clock on the calculation time.
start = time.time()

file = open(f, 'r')
for line in file:
	words = line.split()
	if words[0] == 'DIMENSION:':
			citycount = int(words[1])
	if words[0].isdigit():
		x = [float(words[1]), float(words[2])]
		cities[int(words[0])] = x
	else:
		pass

#Main Operations Section. For each possible starting node, it takes the other nodes and
#sorts them in comparision with the last node visited. It takes the minimum and appends it
#to the visited list, until it loops back to node 1.

#Print comments from testing left in as they make quite a readable printout, if you want
#to see the paths as they are calcuated. 
for starter in [x+1 for x in range(citycount)]:
	unvisited = copy.deepcopy(cities)
	visited = [starter]
	del unvisited[starter]
	totaldistance = 0
	#print starter, cities[visited[-1]]
	while unvisited:
		#print unvisited
		city = min(unvisited.keys(), key=lambda c: distance_math(cities[c], cities[visited[-1]]))
		totaldistance = totaldistance + distance_math(cities[visited[-1]], cities[city])
		visited.append(city)
		del unvisited[city]
		
	totaldistance = totaldistance + distance_math(cities[visited[-1]], cities[starter])
	visited.append(starter)
	#print totaldistance
	if shortestdistance > totaldistance:
		shortestdistance = totaldistance
		shortestpath = copy.deepcopy(visited)
print 'Distance', shortestdistance
print "And it's path", shortestpath
print repr(time.time()-start), 'is the runtime.'
