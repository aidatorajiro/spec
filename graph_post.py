import re
import matplotlib.pyplot as plt
import numpy as np
import os
import shelve
from scipy.sparse import lil_matrix, csr_matrix, load_npz, save_npz
import math
from scipy.spatial import cKDTree

if __name__ == "__main__":
    nodeid_to_pos = np.load(os.path.dirname(__file__) + '/graph_pre_nodeid_to_pos.npz')['arr_0']
    graph_csr = load_npz(os.path.dirname(__file__) + '/graph_pre_graph_csr.npz')
    graph_lil = lil_matrix(graph_csr)
    kdt = cKDTree(nodeid_to_pos)
    N = len(nodeid_to_pos)
    percentage = 0
    r = 1
    print("run with parameter r = %s" % r)
    sum_ball_point = 0
    for i in range(N):
        if i % (N // 100) == 0:
            print(str(percentage) + "%")
            percentage += 1
        ball_point = kdt.query_ball_point(nodeid_to_pos[i], r)
        for j in ball_point:
            point_from = nodeid_to_pos[i]
            point_to = nodeid_to_pos[j]
            distance = math.sqrt(((point_from - point_to)**2).sum())
            graph_lil[i,j] = distance
            graph_lil[j,i] = distance
        if len(ball_point) == 0:
            print("Warning: no neighbor found for index %s" % i)
        sum_ball_point += len(ball_point)
    print("average neighbors: %s" % (sum_ball_point/N))
    
    np.savez_compressed(os.path.dirname(__file__) + '/graph_post_nodeid_to_pos', nodeid_to_pos)
    
    save_npz(os.path.dirname(__file__) + '/graph_post_graph_csr', csr_matrix(graph_lil))
