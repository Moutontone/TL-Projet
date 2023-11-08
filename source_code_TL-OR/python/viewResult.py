import tkinter
from fileReader import *
import sys

#######################################################
# Author: Nicolas Besson                              #
# TL-OR: Project                                      #
#######################################################

def drawPoint(canvas, x, y, color="green"):
    canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color)

def drawDepot(canvas, x, y):
    canvas.create_rectangle(x-5, y-5, x + 5, y + 5, fill="red")

def drawLine(canvas, p1, p2):
    [x1, y1] = p1
    [x2, y2] = p2
    canvas.create_line(x1*w//1280, y1*h//720, x2*w//1280, y2*h//720, fill="purple")

def drawPath(canvas, points, path):
    for i, p in enumerate(path[:-1]):
        drawLine(canvas, points[p], points[path[i + 1]])

def drawCostAllocation(canvas, points, allocation):
    for i, y in enumerate(allocation):
        if points[i][0] <= 1210:
            canvas.create_text(points[i][0]*w//1280 + 35, points[i][1]*h//720 - 10, text=str(round(y, ndigits=2)), fill="blue")
        else:
            canvas.create_text(points[i][0]*w//1280 - 35, points[i][1]*h//720 - 10, text=str(round(y, ndigits=2)), fill="blue")

if __name__ == "__main__":
    top = tkinter.Tk()
    h = 900
    w = 1600
    canvas = tkinter.Canvas(top, height=h, width=w, bg="black")

    nbClients, nbFarmers, capacity, locationCost, costPerKm = readInfoInstanceFile("../data/info_instance.txt")

    coords = readCoordFile("../data/coordinates.txt")
    route = readSolutionFile(sys.argv[2])
    allocation = readAllocationFile(sys.argv[3])
    depots = readDepotsFile(sys.argv[1])

    for d in depots:
        drawDepot(canvas, coords[d][0]*w//1280, coords[d][1]*h//720)
    drawCostAllocation(canvas, coords[1:], allocation)
    color = "green"
    for i, [x, y] in enumerate(coords[1:]):
        if i == nbFarmers:
            color = "yellow"
        drawPoint(canvas, x*w//1280, y*h//720, color)
    drawPath(canvas, coords, route)
    canvas.grid(row=0, column=0)
    top.mainloop()
