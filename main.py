from scipy.sparse import lil_matrix, csr_matrix, load_npz, save_npz
import numpy as np
import sys
import time
import re
import os
import scipy
import json
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler, HTTPStatus
from scipy.spatial import cKDTree

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

nodeid_to_pos = np.load(os.path.dirname(os.path.abspath(__file__)) + '/graph_post_nodeid_to_pos.npz')['arr_0']
graph_csr = load_npz(os.path.dirname(os.path.abspath(__file__)) + '/graph_post_graph_csr.npz')
# graph_lil = lil_matrix(graph_csr)
kdt = cKDTree(nodeid_to_pos)

def get_shortest_path(id_from, id_to):
    solution = solve(id_from, id_to, graph_csr)
    if solution == None:
        return None
    else:
        return [[i, nodeid_to_pos[i].tolist()] for i in solution]

def get_nearest_node(x, y):
    solution = kdt.query(np.array([x, y]))[1]
    return [solution, nodeid_to_pos[solution].tolist()]

def solve(start_index, destination_index, matcsr):
    result = scipy.sparse.csgraph.shortest_path(matcsr, return_predecessors=True, indices=start_index)[1]

    current_index = destination_index
    index_list = [destination_index]

    while True:
        current_index = result[current_index]
        index_list.append(current_index)
        if current_index < 0:
            return None
        if current_index == start_index:
            break
    
    return index_list

class MyHttpRequestHandler(BaseHTTPRequestHandler):
    server_version = "HTTP Stub/0.1"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        args = self.path.split("/")[1:]
        if len(args) == 0:
            text = '{"error": "no argument"}'
        elif args[0] == 'get_shortest_path' and len(args) == 3:
            id_from = int(args[1])
            id_to = int(args[2])
            text = json.dumps({"result": get_shortest_path(id_from, id_to)}, cls = MyEncoder)
        elif args[0] == 'get_nearest_node' and len(args) == 3:
            x = float(args[1])
            y = float(args[2])
            text = json.dumps({"result": get_nearest_node(x, y)}, cls = MyEncoder)
        else:
            text = '{"error": "invalid arguments"}'
        
        encoded = text.encode()

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "applicaton/json; charset=UTF-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(encoded)

def run(server_class=ThreadingHTTPServer, handler_class=MyHttpRequestHandler):
    server_address = ('', int(os.environ['PORT'] if 'PORT' in os.environ else 8000))
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()