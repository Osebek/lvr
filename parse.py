#!/usr/bin/env python

from __future__ import print_function

import sys
import numpy as np
import random
import argparse
values =  {}

def parse(handle):
    formula = []
    valid = (l for l in handle if len(l) > 0 and l[0] not in ("c", "p"))
    for line in valid:
        formula.append([int(lit) for lit in line.split() if int(lit) != 0])
    return formula

def hasEmptyClause(Formula):
    for clause in Formula:
        if len(clause) == 0:
            return True
        return False

def simplify(formula):
    """Simplifiy formula according to the rules"""
    run = True
    while run:
        run = False
        for clause in formula:
            if len(clause) == 1:
                formula = setValueAndReduce(clause[0], 1, formula)
                run = True
                break
    return formula

def setValueAndReduce(Literal,value,Formula):
    """
    Literal ... the literal that we are setting the value to
    value ... the truth value of a literal, can be 1 or -1
    Formula ... the formula that we are reducing

    We set the value of a literal. The clauses in Formula that have
    a literal with a value "T" are removed and literals with
    values "F" are removed from clauses that contain them.
    """
    val = Literal * value
    values[abs(Literal)] = val
    newFormula = []
    for clause in (c for c in Formula if val not in c):
        newClause = []
        for literal in clause:
            if literal != -Literal:
                newClause.append(literal)
        newFormula.append(newClause)
    return newFormula

def getRandomElement(permutation):
    """Returns first viable element from permutation"""
    for clause in permutation:
        if len(clause) != 0:
            return clause[random.randint(0,len(clause)-1)]

def dpll(formula):
    """Main function of the dpll algorithm, works recursively. """
    formula = simplify(formula)
    if len(formula) == 0:
        return True
    if hasEmptyClause(formula):
        return False
    el = getRandomElement(np.random.permutation(formula))
    if dpll(setValueAndReduce(el, 1, formula)):
        return True
    return dpll(setValueAndReduce(el, -1, formula))

def parse_args():
    parser = argparse.ArgumentParser(description = "Simple sat solver")
    parser.add_argument("-i",
                        "--input",
                        help = "read from given file instead of stdin.",
                        type = argparse.FileType("r"),
                        default = sys.stdin)
    parser.add_argument("-o",
                        "--output",
                        help = "write to given file instead of stdout.",
                        type = argparse.FileType("w"),
                        default = sys.stdout)
    return parser.parse_args()

def main():
    args = parse_args()
    formula = parse(args.input)
    sat = dpll(formula)
    if sat:
        args.output.write(" ".join(str(n) for n in values.values()))
    args.output.write("\n")
    sys.exit(0 if sat else 1)

if __name__ == "__main__":
    main()
