import re
import matplotlib.pyplot as plt
import numpy
import os
import shelve

if __name__ == "__main__":
    shel = shelve.open(os.path.dirname(os.path.abspath(__file__)) + "/roads.shel")
    roads = shel['roads']
    for road in roads[-10:-1]:
        arr = numpy.array(road)
        plt.plot(arr[:, 0], arr[:, 1])
    plt.show()