# Collection of (malfunctioning) SAT solvers

This repository contains couple of SAT solvers that were developed during as a
project in "Logic in Programming" course. As title already stated, not all of
them are functional, so take caution when using results in real world.


## Naive implementation of DPLL algorithm

*NOTE:* This implementation used parts of the `numpy` library, so before trying to run
it, make sure numpy is installed.

Naive implementation can be found in `naive_solver.py`. For brief usage
instructions simply execute `naive_solver.py -h`. Typical invocations would
be:

    ./naive_solver.py -i input.dimacs               # Print result into stdout
    ./naive_solver.py -i input.dimcas -o result.txt # Place result in file
    ./naive_solver.py -o result.txt                 # Read dimcas from stdin

Exit code of the solver indicates whether input formula is satisfiable. Zero
return status means success and one means not satisfiable.


## Samples

Some relatively large and quite hard examples that naive implementation can
solve in cca. 20 seconds can be found in `samples` folder.


## Authors

  * Nejc Vesel
  * Tadej Borovšak
