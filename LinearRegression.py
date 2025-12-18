from __future__ import division
import matplotlib.pyplot as plt
# import numpy as np

coords = [(2, 4), (3, 5), (5, 7), (7, 10), (9, 15)]
    
def LinearRegression(coords_list):
    # Takes a list of coordinates as tuples and returns the regression line in the same format.
    reg_list = []
    n = len(coords_list)
    sumx, sumy, sumx2, sumxy = 0, 0, 0, 0
    for x, y in coords_list:
        sumx += x
        sumy += y
        sumx2 += x*x
        sumxy += x*y
    m = (n*sumxy - sumx * sumy) / (n*(sumx2) - (sumx)**2)
    b = (sumy - m*(sumx)) / n
    for x, y in coords_list:
        calc_y = (m*x) + b
        error = y - calc_y
        ords = (x, calc_y)
        reg_list.append(ords)
        print "\nx = {}, y = {}, calculated y = {}, error = {}".format(x, y, calc_y, error)
    print "\nSlope = {}, intercept = {}".format(m, calc_y)
    return reg_list
    
def PlotLines(ords_list):
    reg_ords = LinearRegression(ords_list)
    xords = [ord[0] for ord in ords_list]
    yords = [ord[1] for ord in ords_list]
    reg_yords = [ord[1] for ord in reg_ords]
    fig, ax = plt.subplots()
    ax.plot(xords, yords)
    ax.plot(xords, reg_yords)
    ax.set(xlabel='x', ylabel='y', title='About as simple as it gets, folks')
    ax.grid()
    plt.show()
        
