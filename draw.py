import re
import matplotlib.pyplot as plt
import numpy as np
import os
import shelve
from scipy.sparse import lil_matrix, csr_matrix, load_npz, save_npz
import math
from scipy.spatial import cKDTree

def tostr(pos):
    return str(pos[0]) + str(pos[1])

if __name__ == "__main__":
    nodeid_to_pos = np.load(os.path.dirname(os.path.abspath(__file__)) + '/graph_post_nodeid_to_pos.npz')['arr_0']
    graph_csr = load_npz(os.path.dirname(os.path.abspath(__file__)) + '/graph_post_graph_csr.npz')
    graph_lil = lil_matrix(graph_csr)
    d = ""
    for [i, j] in zip(graph_lil.nonzero()[0], graph_lil.nonzero()[1]):
        if i < j: 
            d += "M " + tostr(nodeid_to_pos[i]) + " " + tostr(nodeid_to_pos[j]) + " Z "
    
    svg = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   id="svg8"
   version="1.1"
   viewBox="0 0 2870.553 1425.575"
   height="1425.575mm"
   width="2870.553mm">
  <defs
     id="defs2" />
  <metadata
     id="metadata5">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     transform="translate(0,1128.575)"
     id="layer1">
    <path
       id="path196"
       d=\"""" + d + """\"
       stroke="green" />
  </g>
</svg>
"""
    with open("post.svg", "w") as f:
        f.write(svg)
