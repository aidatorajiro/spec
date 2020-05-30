import re
import matplotlib.pyplot as plt
import numpy
import os
import shelve

roads = shelve.open(os.path.dirname(__file__) + "/roads.shel")['roads']

