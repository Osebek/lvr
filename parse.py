import numpy as np

values =  {}

def readDimacs(file):
    lines = [line.rstrip('\n') for line in open(file)]
    Formula =      [[ int(n) for n in line.split() if  int(n) != 0 ]\
    for line in lines if line[0] not in ('c', 'p')]
    return Formula

def hasEmptyClause(Formula):
	for clause in Formula:
		if len(clause) == 0:
			return True
		return False

def canBeSimplified(Formula):
	for clause in Formula:
		if isinstance(clause,int):
			return True
		elif len(clause) == 1:
			return True

	return False

def checkClause(clause, negatives, replace):
	newClause = []
	for literal in clause:
		if literal in replace:
			return []
		if literal not in negatives:
			newClause.append(literal)
	return newClause

def simplify(Formula):
	replace = {}
	negatives = {}
	newFormula = []
	for clause in Formula:
		if isinstance(clause, int):
			replace[clause] = clause
			negatives[-clause[0]]= -clause[0]
		elif len(clause) == 1 and isinstance(clause[0],int):
			replace[clause[0]] = clause[0]
			negatives[-clause[0]] = -clause[0]


	values.update(replace)
	for clause in Formula:
		clause = checkClause(clause, negatives,replace)
		if len(clause) != 0:
			newFormula.append(clause)

	return newFormula

def opposite(Value):
	if Value == 'T':
		return 'F'
	elif Value =='F':
		return 'T'
def containsTorF(clause):
	for literal in clause:
		if not isinstance(literal, clause):
			return literal

	return "N"


def reduce(Formula):
	newFormula = []
	for clause in Formula:
		val = containsTorF(clause)
		if "N" == val:
			newFormula.append(clause)
		elif "F" == val:
			newFormula.append([])
		
				

def setValue(Literal,Value,Formula):
	newFormula = []
	for clause in Formula:
		newClause = []
		for literal in clause:
			if literal == Literal:
				literal = Value
			elif literal == -Literal:
				literal = opposite(Value)
			newClause.append(literal)
		
		newFormula.append(newClause)

	if Value == "T":
		values[Literal] = Literal
	else:
		values[-Literal] = -Literal
		
	return newFormula 
	
def readAndSortSolution(file):
	lines = [line.rstrip('\n') for line in open(file)]
	solution =      [[ int(n) for n in line.split() if  int(n) != 0 ]\
    for line in lines]
	return sorted(solution[0])





def dpll(Formula):
	if len(Formula) == 0:
		return ("SAT",sorted(values.values()))
	elif hasEmptyClause(Formula):
		return "UNSAT"
	elif canBeSimplified(Formula):
		return dpll(simplify(Formula))
	else:
		el = np.random.permutation(Formula)[0][0]
		if dpll(reduce(setValue(el,"T", Formula))) == "SAT":
			return "SAT"
		else:
			return dpll(reduce(setValue(el,"F", Formula)))







	
Formula = readDimacs("sudoku1.txt")

(SAT, solP) =  dpll(Formula)
solT = readAndSortSolution("sudoku1_solution.txt")
print solT == solP



