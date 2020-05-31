import re
import matplotlib.pyplot as plt
import numpy
import os
import shelve
from svgparse import *

if __name__ == "__main__":
    with open(os.path.dirname(os.path.abspath(__file__)) + "/roads.svg") as f:
        svg = f.read()
    d = re.search(r' d="(.+?)"', svg)[1]
    parsed = parse_d(d)
    round_dbl_array(parsed)
    shel = shelve.open(os.path.dirname(os.path.abspath(__file__)) + "/roads.shel")
    shel['roads'] = parsed