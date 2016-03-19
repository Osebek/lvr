def readDimacs(file):
    lines = [line.rstrip('\n') for line in open(file)]
    allClauses =      [[ int(n) for n in line.split() if  int(n) != 0 ]\
    for line in lines if line[0] not in ('c', 'p')]
    return allClauses


