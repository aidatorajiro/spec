import re
import matplotlib.pyplot as plt
import numpy as np
import os
import shelve
from svgparse import *
import json

if __name__ == "__main__":
    prefix = "lroc_color_poles_8kg"
    # levels = [240, 200, 150]
    levels = ["240"]
    buildings = {}
    for l in levels:
        buildings[l] = []
        dataname = prefix + l
        with open(os.path.dirname(os.path.abspath(__file__)) + "/" + dataname + ".svg") as f:
            svg = f.read()
        d = re.search(r' d="(.+?)"', svg)[1]
        parsed = parse_d(d)
        round_dbl_array(parsed)
        for blob in parsed:
            arr = np.array(blob)
            g = arr.sum(0)/len(blob) # calc center of gravity
            buildings[l].append(g.tolist())
    with open(os.path.dirname(os.path.abspath(__file__)) + "/buildings.js", "w") as f:
        f.write("let buildings = ")
        json.dump(buildings, f)
