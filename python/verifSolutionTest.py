from verifSolution import *

# No arc leaving depot, INCORRECT SOLUTION
verifTest1 = [[[0, 0, 0, 0, 0],
               [0, 0, 1, 0, 0],
               [0, 1, 0, 0, 0],
               [1, 0, 0, 0, 0],
               [0, 0, 0, 1, 0]]]
assert verifSol(verifTest1, 5, 1) == False

# Flow constraints not respected, INCORRECT SOLUTION
verifTest2 = [[[0, 0, 0, 1, 0],
               [0, 0, 1, 0, 0],
               [0, 0, 0, 1, 0],
               [1, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]]]
assert verifSol(verifTest2, 5, 1) == False

# Two seperate loops in one tour, INCORRECT SOLUTION
verifTest3 = [[[0, 0, 0, 1, 0],
               [0, 0, 0, 0, 1],
               [0, 1, 0, 0, 0],
               [1, 0, 0, 0, 0],
               [0, 0, 1, 0, 0]]]
assert verifSol(verifTest3, 5, 1) == False

# Out degree > 1 on a farmer, INCORRECT SOLUTION
verifTest4 = [[[0, 0, 0, 1, 0],
               [0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0],
               [0, 1, 0, 0, 0],
               [0, 0, 1, 0, 1]]]
assert verifSol(verifTest4, 5, 1) == False

# Two valid loops in one tour, INCORRECT SOLUTION
verifTest5 = [[[0, 0, 0, 1, 0],
               [0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0],
               [1, 1, 0, 0, 0],
               [0, 0, 1, 0, 0]]]
assert verifSol(verifTest5, 5, 1) == False

# Single correct loop, CORRECT SOLUTION
verifTest6 = [[[0, 0, 0, 1, 0],
               [0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0],
               [0, 1, 0, 0, 0],
               [0, 0, 1, 0, 0]]]
assert verifSol(verifTest6, 5, 1) == True

# Two correct loops on 2 tours, CORRECT SOLUTION
verifTest7 = [[[0, 0, 0, 1, 0],
               [0, 0, 0, 0, 1],
               [0, 0, 0, 0, 0],
               [0, 1, 0, 0, 0],
               [1, 0, 0, 0, 0]],
              [[0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]]]
assert verifSol(verifTest7, 5, 2) == True

# Correct single loop + second correct loop, INCORRECT SOLUTION
verifTest8 = [[[0, 0, 0, 1, 0],
               [0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0],
               [0, 1, 0, 0, 0],
               [0, 0, 1, 0, 0]],
              [[0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]]]
assert verifSol(verifTest8, 5, 2) == False

# Two correct loops on 2 tours and one empty tour, CORRECT SOLUTION
verifTest7 = [[[0, 0, 0, 1, 0],
               [0, 0, 0, 0, 1],
               [0, 0, 0, 0, 0],
               [0, 1, 0, 0, 0],
               [1, 0, 0, 0, 0]],
              [[0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]],
              [[0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]]]
assert verifSol(verifTest7, 5, 3) == True

print('\nAll Tests have passed\n')
