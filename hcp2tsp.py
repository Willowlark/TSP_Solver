import os, sys

#Inital Declarations
file = os.sys.argv[1]
name = ''
type = ''
dim = 0
test = 1
ordernum = -1

f = open(file, 'r')

currentnum = 0
storearr = []

'''Reads in the hcp and processes it on the go.
It's done by breaking down the edge list into it's
subparts, which are divided by the larger node. Order
doesn't matter. For that larger edge, each connection is
stored and then the blanks and those are filled in to the
line that will be printed to the tsp file. Checks are included
for nodes that have no edges while under the largest edge, or
just no edges. because of the lower diagonal format, it fills in
the required values.'''

for line in f:                 # N cities + 8 or something info lines
	#basic read ins.
	words = line.split()
	if words[0] == "NAME:":
		name = words[1]

	elif words[0] == "TYPE:":
		type = words[1]

	elif words[0] == "DIMENSION:" or words[0] == "DIMENSION":
		dim = int(words[1])

	elif words[0].isdigit():
		ichi = int(words[0])
		ni = int(words[1])
		if ichi < ni:
			ichi, ni = ni, ichi
		storearr.append([ichi,ni])

	else:
		if test: print "I've got a bad feeling about this.", words[0]
f.close()

storearr.sort(key=lambda x: (x[0],x[1]))

f = open('tspfile.tsp', 'w')

#Write out the string just generated and header info.
f.write( """\
NAME : {0}
COMMENT : Auto generated.
TYPE : TSP
DIMENSION : {1}
EDGE_WEIGHT_TYPE: EXPLICIT
EDGE_WEIGHT_FORMAT: LOWER_DIAG_ROW
EDGE_WEIGHT_SECTION
""".format(name, dim))

if test: print storearr
for x in range(1,dim+1):
	for y in range(1,x+1):
		if len(storearr) > 0 and [x,y] == storearr[0]:
			f.write('1\n')
			storearr.pop(0)
		elif x == y:
			f.write('0\n')
		else:
			f.write('2\n')
f.write('EOF')
f.close()

#Call the system for running concorde on the created file.
os.system("~/concorde/TSP/concorde ~/git/potential-avenger/tspfile.tsp > concordereturn")
f = open('concordereturn', 'r')

#Search the answer output for the optimal solution and use it to make a decision.
ans = -1
for i in f:
	if i.strip() != '' and i.strip().split()[0] == 'Optimal':
		x = i.split()
		ans = int(float(x[2]))
		break
if dim == ans:
	print 'A cycle exists. Optimal Tour: ', ans
else:
	print 'No cycle present. Optimal Tour: ', ans
