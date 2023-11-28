################## Solution Verification ######################
def verifSol(mat, n, t):
  verifVisited = [False for i in range(n)]
  verifAxis = [False for i in range(n)]
  verifOrd = [False for i in range(n)]
  verifValid = True
  verifPointer = 0
  nextJ = 0
  for t in range(t):
    verifPointer = 0
    nextJ = 0
    for i in range(n):
      for j in range(n):
        if mat[t][verifPointer][j] == True:
          if verifVisited[verifPointer] == True and verifPointer != 0:
            verifValid = False
          verifVisited[verifPointer] = True
          verifAxis[verifPointer] = True
          verifOrd[j] = True
          nextJ = j
      verifPointer = nextJ
      if verifPointer == 0:
        break
    for i in range(n):
      if verifAxis != verifOrd:
        verifValid = False
  for i in range(n):
    if verifVisited[i] == False:
      verifValid = False
  return verifValid

