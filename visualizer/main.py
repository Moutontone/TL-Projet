import matplotlib.pyplot as plt
import numpy as np

# data
F = [(-1, 1), (-1.4, -2)]
C = [(1.5, 2), (3, -0.3)]
D = (0,0)

path_farmer = [F[0], F[1]]
path_client = [C[0], C[1]]

# parameters

size = 300
size_depot = 600
mark_farmers = "s"
color_farmers = "red"

mark_depot = "p"
color_depot = "purple"

mark_clients = "o"
color_clients = "green"

# functions

def plot_locations(farmers, clients, ax):
    # plot Depot
    ax.scatter(0,0, marker = mark_depot, color = color_depot, sizes=[size_depot])

    # plot Farmers
    X, Y = [], []
    for fx, fy in farmers:
        X.append(fx)
        Y.append(fy)
    ax.scatter(X,Y, marker = mark_farmers, color = color_farmers, sizes=[size]*len(X))

    # plot Client
    X, Y = [], []
    for fx, fy in clients:
        X.append(fx)
        Y.append(fy)
    ax.scatter(X,Y, marker = mark_clients, color = color_clients, sizes=[size]*len(X))

# plot path
def plot_path(path, ax, color):
    X, Y = [0], [0]
    for x, y in path:
        X.append(x)
        Y.append(y)
    X.append(0)
    Y.append(0)
    ax.plot(X,Y, color = color, zorder=-1)
    for i in range(1, len(X)):
        x = X[i - 1]
        y = Y[i - 1]
        dx = (X[i - 1] + X[i])/2 - x
        dy = (Y[i - 1] + Y[i])/2 - y
        plt.arrow(x, y, dx, dy, shape='full', lw=0, color = color, length_includes_head=True, head_width=.15)

fig, ax = plt.subplots()

plot_path(path_farmer, ax, "black")
plot_path(path_client, ax, "blue")
plot_locations(F, C, ax)

plt.show()
