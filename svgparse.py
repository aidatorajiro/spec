import re
import matplotlib.pyplot as plt
import numpy
import os
import shelve

def parse_d(data, ignore_z=False):
    current_mode = "none"
    
    if ignore_z:
        points = []
    else:
        points = [[]]
    
    current_x = 0
    current_y = 0
    args = []
    
    def debug_err(message):
        print(current_mode)
        print(current_x)
        print(current_y)
        raise Exception(message)
    
    for command in data.split(" "):
        if re.match(r"^[a-zA-Z]$", command):
            if current_mode in "mlML":
                for [x, y] in args:
                    if current_mode in "ml":
                        abs_x = x + current_x
                        abs_y = y + current_y
                    else:
                        abs_x = x
                        abs_y = y
                    if ignore_z:
                        points.append([abs_x, abs_y])
                    else:
                        points[-1].append([abs_x, abs_y])
                    current_x = abs_x
                    current_y = abs_y
            elif current_mode in "hvHV":
                for a in args:
                    if current_mode in "h":
                        abs_x = current_x + a
                        abs_y = current_y #
                    if current_mode in "v":
                        abs_x = current_x #
                        abs_y = current_y + a
                    if current_mode in "H":
                        abs_x = a
                        abs_y = current_y #
                    if current_mode in "V":
                        abs_x = current_x #
                        abs_y = a
                    if ignore_z:
                        points.append([abs_x, abs_y])
                    else:
                        points[-1].append([abs_x, abs_y])
                    current_x = abs_x
                    current_y = abs_y
            elif (not ignore_z) and current_mode in "zZ":
                points.append([])
            
            args = []
            
            if command in "mzlhvMZLHV":
                current_mode = command
            else:
                raise Exception("unrecognized command")
        elif re.match(r"^[e\-\d\.]+,[e\-\d\.]+$", command):
            [a, b] = command.split(",")
            args.append([float(a), float(b)])
        elif re.match(r"^[e\-\d\.]+$", command):
            args.append(float(command))
        else:
            print(command)
            debug_err("unrecognized argument")
    
    return points

def round_dbl_array(a, prec=3):
    for i in range(len(a)):
        for j in range(len(a[i])):
            a[i][j][0] = round(a[i][j][0], prec)
            a[i][j][1] = round(a[i][j][1], prec)

if __name__ == "__main__":
    with open(os.path.dirname(__file__) + "/roads.svg") as f:
        svg = f.read()
    d = re.search(r' d="(.+?)"', svg)[1]
    parsed = parse_d(d)
    round_dbl_array(parsed)
    shel = shelve.open(os.path.dirname(__file__) + "/roads.shel")
    shel['roads'] = parsed