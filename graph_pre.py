import re
import matplotlib.pyplot as plt
import numpy as np
import os
import shelve
from scipy.sparse import lil_matrix, csr_matrix, save_npz
import math

def inv_list(lst):
    out = {}
    for k, v in enumerate(lst):
       out[v] = k
    return out

def from_posstr(posstr):
    [xst, yst] = posstr.split(" ")
    return [float(xst), float(yst)]

def to_posstr(point):
    # return id(point)   Wow black magick!
    return str(point[0]) + " " + str(point[1])

def calc_distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

if __name__ == "__main__":
    roads = shelve.open(os.path.dirname(os.path.abspath(__file__)) + "/roads.shel")['roads']
    
    nodeset = set()
    
    for road in roads:
        for point in road:
            nodeset.add(to_posstr(point))
    
    N = len(nodeset)
    
    print("# of nodes: " + str(N))
    
    nodeid_to_posstr = list(nodeset)
    posstr_to_nodeid = inv_list(nodeid_to_posstr)
    nodeid_to_pos = np.array(list(map(from_posstr, nodeid_to_posstr))) # to save
    graph_lil = lil_matrix((N, N), dtype=np.float32) # to save
    
    print("calculating pre graph_lil...")
    
    for road in roads:
        str_from = to_posstr(road[0])
        point_from = road[0]
        for point_to in road[1:]:
            str_to = to_posstr(point_to)
            
            id_from = posstr_to_nodeid[str_from]
            id_to = posstr_to_nodeid[str_to]
            
            if id_from != id_to:
                distance = calc_distance(point_from, point_to)
            
                graph_lil[id_from,id_to] = distance
                graph_lil[id_to,id_from] = distance
            
            str_from = str_to
            point_from = point_to
    
    print("complete! saving...")
    
    np.savez_compressed(os.path.dirname(os.path.abspath(__file__)) + '/graph_pre_nodeid_to_pos', nodeid_to_pos)
    
    save_npz(os.path.dirname(os.path.abspath(__file__)) + '/graph_pre_graph_csr', csr_matrix(graph_lil))
