'''Best first search solver for the TSP Problem
Author Bill Clark unless otherwise noted
Contributors John To, Craig'''


from sys import maxint
from sys import argv
from math import sqrt
from time import time

#Gobal Variables
reality = maxint #Lowest tour
citycount = 0 #number of cties in problem
cities = [] #stores city x at x-1 as an ordered pair list.
leaves = [] #stores lists of city id and it's node.
shortest = [] #shortest permutation
matrix =[] #the distance between city a,b.

#Does the distance formula on two lists of an ordered pair.
def distance_math(one, two):
	x = sqrt((two[0] - one[0])**2 + (two[1] - one[1])**2)
	return x

#Given a list of cities, adds up their distances from each other in order.
def path_distance(list):
	total = 0
	for x in range(0,len(list)-1):
		one = list[x]
		two = list[x+1]
		pair = sorted([one, two])
		total+= matrix[pair[0]][pair[1]]
	return total

#A mostly container class for a node on the 'tree'.
#Initalizes with the path you took to get here, including self,
#an id for it's source city, and it's bound, which is calculated
#internally.
class Node:
	def __init__(self, ident, path):
		self.path = path
		#print self.path
		self.id = ident
		self.path.append(self.id)
		self.dream = self.bound()

	#Originally the operation was recursive inside of node.
	#There were scope issues though, and it wouldn't leave
	#path as an instance variable. Took everything out of node
	#As a fix, keeping original for records.
	'''def run(self):
		global reality
		global leaves
		spath = sorted(self.path)

		if [x for x in range(1,citycount+1)] == spath:
			self.path.append(1)
			y = path_distance(self.path)
			if reality > y:
				reality = y
				shortest = self.path
				for x in range(0, len(leaves)): #prune part
					if y < leaves[x][1].dream:
						leaves.pop(x)
				if len(leaves) == 0:
					print 'finished.'
					#return 'desu'
				else:
					leaves = sorted(leaves, key=lambda leaf: leaf[1].dream)
					#print leaves
					leaves[0][1].run()
		else:
			for x in range(1,citycount+1):
				if x not in self.path:
					y = Node(x,self.path)
					leaves.append([x,y])
			leaves = sorted(leaves, key=lambda leaf: leaf[1].dream)
			#print leaves
			leaves[0][1].run()'''

	#Calculates the bound of a node, Making sure to include edges that
	#already were travelled. It does those checks via the path list.
	def bound(self):
		total = 0
		for x in range(1,citycount+1):
			append1 = 0
			append2 = 0
			arr = matrix[x][:]
			#print arr
			arr.pop(x)
			arr.pop(0)
			if x in self.path and len(self.path) != 1:
				if self.path[-1] == x:
					append1 = matrix[self.path[-2]][self.path[-1]]
					arr.remove(append1)
				elif self.path[0] == x:
					append1 = matrix[self.path[0]][self.path[1]]
					arr.remove(append1)
				else:
					append1 = matrix[self.path[-2]][self.path[-1]]
					append2 = matrix[self.path[0]][self.path[1]]

			if not append1:
				append1 = min(arr)
				arr.remove(append1)
			if not append2:
				append2 = min(arr)
				arr.remove(append2)
			total+= append1+append2
		total = total/2
		return total

#Asks for a file, then reads in ordered pairs.
file = 0
if len(argv) > 1:
	file = f = open(argv[1], 'r')
else:
	f = raw_input("enter filename: ")
	file = open(f, 'r')

for line in file:
	words = line.split()
	if words[0] == 'DIMENSION:' or words[0] == 'DIMENSION':
		citycount = int(words[1])
	if words[0].isdigit():
		x = [int(float(words[1])), int(float(words[2]))]
		cities.append(x)
	else:
		pass
print 'file read.'

#begins the timer.
start = time()

# Distance double array builder by John To. Stores cities in a double array,
# which can be used with two city ids to get the distance between them.
matrix = [[0 for i in xrange(citycount+1)] for i in xrange(citycount+1)]
for i in range(1,citycount+1):
	for j in range(1,citycount+1):
		matrix[i][j] = distance_math(cities[i-1], cities[j-1])
print 'matrix generated.'

#creates the first node and puts it in the leaves, which dictates
#the operation loop's end condition.
first_node = Node(1,[])
leaves.append([1, first_node])
its = 0
citylist = set([x for x in range(1,citycount+1)])
# While there are leaves available, choose the best one. if it's a full
# path, prune on it's path_distance and resume if there are unpruned better
# options. Else it will generate the children for the current leaf,
# then return to start.
while len(leaves) > 0:
	#leaves = sorted(leaves, key=lambda leaf: leaf[1].dream)
	leaves.sort(key = lambda x: (x[1].dream, len(x[1].path)))
	its+=1
	function_node = leaves.pop(0)[1]
	#spath = sorted(function_node.path)

	#if [x for x in range(1,citycount+1)] == spath:
	if citycount == len(function_node.path):
		function_node.path.append(1)
		y = path_distance(function_node.path)
		if reality > y:
			reality = y
			shortest = function_node.path
			leaves = [x for x in leaves if reality > x[1].dream] #pruning
			#print 'path checked.', function_node.path, reality, function_node.dream
			if len(leaves) == 0:
				print 'finished.'
				break
	else:
		z = list(set(citylist) - set(function_node.path))
		for x in z:
			y = Node(x,function_node.path[:])
			leaves.append([x,y])
		leaves = [x for x in leaves if reality > x[1].dream] #prune function
		#print function_node.path, reality, function_node.dream
print reality, shortest, 'Time: ', time()-start, 'iterations: ', its