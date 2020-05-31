# Before running, prepare roads.svg and lroc_color_poles_8kg240.svg

python3 svgparse_road.py
python3 graph_pre.py
python3 graph_post.py
python3 draw.py
python3 graph_json.py
python3 svgparse_building.py

# After running this, please convert post.svg to post.png or jpg using inkscape