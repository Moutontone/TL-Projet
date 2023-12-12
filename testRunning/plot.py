import matplotlib.pyplot as plt

fileO0 = open('testRunning/solvingTimesO0.txt', 'r')
fileO1 = open('testRunning/solvingTimesO1.txt', 'r')
fileO2 = open('testRunning/solvingTimesO2.txt', 'r')
dataO0 = [0, 0, 0, 0, 0]
dataO1 = [0, 0, 0, 0, 0]
dataO2 = [0, 0, 0, 0, 0]

for i in range(6):
  meanO1 = 0
  meanO2 = 0
  for j in range(20):
    x1 = int(fileO1.readline())
    meanO1 += -x1
    x2 = int(fileO2.readline())
    meanO2 += -x2
  meanO1 /= 20
  meanO2 /= 20
  dataO1.append(meanO1)
  dataO2.append(meanO2)
for i in range(5):
  meanO0 = 0
  for j in range(15):
    x0 = int (fileO0.readline())
    meanO0 += -x0
  meanO0 /= 15
  dataO0.append(meanO0)
plt.title('Average Execution Time by Instance Size')
plt.xlabel('instance size (nb of farmers)')
plt.ylabel('average execution time (seconds)')
plt.plot(dataO0, label='exponential variable model')
plt.plot(dataO1, label='quadratic variable model')
plt.plot(dataO2, label='quadratic variable & improved tour upperbound')
plt.legend()
plt.show()
