from math import sqrt
from sys import maxint
import copy
import time

#Global vars.
citycount = 0
cities = {}
shortestdistance = maxint
shortestpath = []
start = 0

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

for starter in [x+1 for x in range(citycount)]:
	unvisited = cities.copy()
	visited = [starter]
	del unvisited[starter]
	totaldistance = 0
	
	while unvisited:
		city = min(unvisited.keys(), key=lambda c: distance_math(cities[visited[-1]], cities[c]))
		totaldistance += distance_math(cities[visited[-1]], cities[city])
		visited.append(city)
		del unvisited[city]
	totaldistance += distance_math(cities[visited[-1]], cities[starter])
	visited.append(starter)
	
	if shortestdistance > totaldistance:
		shortestdistance = totaldistance
		shortestpath = copy.deepcopy(visited)
print 'Distance', shortestdistance
print "And it's path", shortestpath
print repr(time.time()-start), 'is the runtime.'
