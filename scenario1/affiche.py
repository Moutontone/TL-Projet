import matplotlib.pyplot as plt
import numpy as np

delta = 87
T0 = 171
alpha = 0.99536
epoch = 2100

X = [x for x in range(epoch)]
T = [T0 * (alpha ** e) for e in X]
Y = [np.exp(-delta/t) for t in T]

plt.plot(X, T)
plt.show()
