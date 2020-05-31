import re
import matplotlib.pyplot as plt
import numpy as np
import os
import shelve
from scipy.sparse import lil_matrix, csr_matrix, load_npz, save_npz
import math
from scipy.spatial import cKDTree

if __name__ == "__main__":
    nodeid_to_pos = np.load(os.path.dirname(os.path.abspath(__file__)) + '/graph_pre_nodeid_to_pos.npz')['arr_0']
    graph_csr = load_npz(os.path.dirname(os.path.abspath(__file__)) + '/graph_pre_graph_csr.npz')
    graph_lil = lil_matrix(graph_csr)
    