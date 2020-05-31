import re
import matplotlib.pyplot as plt
import numpy as np
import os
import shelve
from scipy.sparse import lil_matrix, csr_matrix, load_npz, save_npz
import math
from scipy.spatial import cKDTree
import json

if __name__ == "__main__":
    nodeid_to_pos = np.load(os.path.dirname(os.path.abspath(__file__)) + '/graph_post_nodeid_to_pos.npz')['arr_0']
    with open("graph_post_nodeid_to_pos.json", "w") as f:
        json.dump(nodeid_to_pos.tolist(), f)
    