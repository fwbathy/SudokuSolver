
import sys
import time


def row(i):
    return i // 9

def column(i):
    return i % 9

def box(i):
    return (i // 9 // 3 )*3 + (i // 3) % 3

def isNeighbor(x,y):
	if row(x)==row(y):
		return True
	if column(x)==column(y):
		return True
	if box(x)==box(y):
		return True
	return False


def getFileName():
    if sys.platform == "win32":
            filename = input("Filename? ")
    else:
            filename = sys.argv[-1]
    return filename
    

class Cell(object):
    def __init__(self, value):
        self.value = value
        if value == 0:
            self.candidates = [1,2,3,4,5,6,7,8,9]
        else:
            self.candidates = [value]
    def __str__(self):
        return str(self.value)
    def setValue(self,value):
    	self.value = value
    	self.candidates = [value]
    def getValue(self):
    	return self.value
    def delCandidate(self, value):
        self.candidates = [x for x in self.candidates if x != value]
        if len(self.candidates) == 1:
            self.value = self.candidates[0]
    def canLen(self):
        return len(self.candidates)
    def getCan(self):
        return self.candidates[0]

    def setCan(self, newcan):
        self.candidates = newcan[:]


class Board(object):
    def __init__(self, puzz):
        self.puzzle = []
        index = 0
        while index < 81:
            self.puzzle.append(Cell(int(puzz[index])))
            index += 1
    def __eq__(self, puzz):
        index = 0
        while index < 81:
            if self.puzzle[index].value != puzz.puzzle[index].value:
                return False
            index += 1
        return True
    def __str__(self):
        myStr = ""
        index = 0
        while index < 81:
            myStr += str(self.puzzle[index].value)
            index += 1
        return myStr
    def clearNeighbors(self, index):
    	value = self.puzzle[index].getValue()
    	it = 0
    	while it < 81:
    		if it != index and isNeighbor(it,index):
    			self.puzzle[it].delCandidate(value)
    		it += 1


def solve(board):

    print(board)
    print()
    worklist = [board]
    solutions = []
    boardsGen = 0

    while len(worklist) > 0 and len(solutions) < 2:
        boardsGen += 1
        workboard = worklist.pop()
        sq = 1

        while (sq):
            index = 0
            minimum = -1
            sq = 0
            good = True

            while index < 81:
                if workboard.puzzle[index].canLen() == 0:
                    good = False
                    sq = 0
                    break
                elif workboard.puzzle[index].canLen() == 1:
                    workboard.clearNeighbors(index)
                else:
                    sq += 1
                    if minimum == -1:
                        minimum = index
                    else:
                        if workboard.puzzle[index].canLen() < workboard.puzzle[minimum].canLen():
                            minimum = index
                index += 1

            if (minimum != -1) and good:
                for i in workboard.puzzle[minimum].candidates:
                    newboard = Board(str(workboard))
                    newboard.puzzle[minimum] = Cell(i)
                    k = 0
                    while k < 81:
                        if k != minimum:
                            newboard.puzzle[k].setCan(workboard.puzzle[k].candidates)
                        k += 1
                    newboard.clearNeighbors(minimum)
                    worklist.append(newboard)
                    sq = 0
                    good = 0

        if good:
            original = True
            for i in solutions:
                if i == workboard:
                    original = False
                    break
            if original:
                solutions.append(workboard)

    # print ("Boards generated: ", boardsGen)
    return solutions

#====================================================================================

# main():
print()
print("Results: ")
print("------------------------------------------------------------------------------------------")
print()
with open (sys.argv[1], "r") as myfile:
    data = myfile.read().replace('\n', '')
myfile.close()

# before = time.clock()
# after = time.clock()

soln = solve(Board(data))

if len(soln) == 0:
	print ("There are no solutions.")
if len(soln) == 1:
	print ("There is one solution: ")
if len(soln) > 1:
	print ("There are more than two solutions, but here are two:")

# print("Time: ", after-before, " sec.")
while (len(soln)):
    print (soln.pop())
print()
