#!/usr/bin/env python

from __future__ import print_function

import numpy as np
import random
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
    """Checks if clause contains negatives of single literals
    or literals that are known to be true, so the clauses that
    contain them can be removed"""
    newClause = []
    for literal in clause:
        if literal in replace:
            return []
        if literal not in negatives:
            newClause.append(literal)
    return newClause

def simplify(Formula):
    """Simplifiy formula according to the rules"""
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
    """Determines if a clause contains a literal with a fixed value T or F"""
    for literal in clause:
        if literal == 'T':
            return 'T'
        elif literal == 'F':
            return 'F'

    return "N"

def removeSetValues(clause):
    """ Remove values from a clause that contain literals with fixed values, i.e. 'T' or 'F' """
    newClause = []
    for literal in clause:
        if isinstance(literal,int):
            newClause.append(literal)

    return newClause

def setValueAndReduce(Literal,Value,Formula):
    """
    Literal ... the literal that we are setting the Value to
    Value ... the truth value of a literal, can be 'T' or 'F'
    Formula ... the formula that we are reducing

    We set the value of a literal. The clauses in Formula that have
    a literal with a value 'T' are removed and literals with
    values 'F' are removed from clauses that contain them.
    """
    newFormula = []
    for clause in Formula:
        newClause = []
        for literal in clause:
            if literal == Literal:
                literal = Value
            elif literal == -Literal:
                literal = opposite(Value)
            newClause.append(literal)

        if containsTorF(newClause) == 'N':
            newFormula.append(newClause)
        elif containsTorF(newClause) == 'F':
            newFormula.append(removeSetValues(newClause))

    if Value == "T":
        values[Literal] = Literal
    else:
        values[-Literal] = -Literal
    return newFormula

def readAndSortSolution(file):
    """Read the solution and sort it so that we can compare it to the solution.
    This was needed for testing Sudoku"""
    lines = [line.rstrip('\n') for line in open(file)]
    solution =      [[ int(n) for n in line.split() if  int(n) != 0 ]\
    for line in lines]
    return sorted(solution[0])

def getRandomElement(permutation):
    """Returns first viable element from permutation"""
    for clause in permutation:
        if len(clause) != 0:
            return clause[random.randint(0,len(clause)-1)]




def dpll(Formula):
    """Main function of the dpll algorithm, works recursively. """
    if len(Formula) == 0:
        return ("SAT",sorted(values.values()))
    elif hasEmptyClause(Formula):
        return ("UNSAT", sorted(values.values()))
    elif canBeSimplified(Formula):
        return dpll(simplify(Formula))
    else:
        el = getRandomElement(np.random.permutation(Formula))
        (dpllResult, _) = dpll(setValueAndReduce(el,"T", Formula))
        if dpllResult == "SAT":
            return ("SAT",sorted(values.values()))
        else:
            return dpll(setValueAndReduce(el,"F", Formula))





Formula = readDimacs("sudoku1.txt")

(SAT, solP) =  dpll(Formula)
solT = readAndSortSolution("sudoku1_solution.txt")
print(solP)
print(solT)
print(SAT)


