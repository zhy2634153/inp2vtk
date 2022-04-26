#!/usr/bin/env python3
#-*-coding:utf-8-*-

import re
import numpy as np

inp_fname = "data/Job-1-C3D20.inp"
vtk_fname = inp_fname[:-4]+".vtk"

f_inp = open(inp_fname, 'r')
f_vtk = open(vtk_fname, 'w')

content = f_inp.readlines()
f_inp.close()

flag_node = False
# flag_eles_C3D4, flag_eles_C3D8, flag_eles_C3D10, flag_eles_C3D20
flag_eles = [False, False, False, False]
# flag_ele_C3D8 = False
# flag_ele_C3D20 = False
# flag_ele_C3D4 = False
# flag_ele_C3D10 = False
nodes = []
eles = []
eles = [[],[],[],[]]
eles_C3D20 = []

# cell_types = [CELL_TYPE_C3D4, CELL_TYPE_C3D8, CELL_TYPE_C3D10, CELL_TYPE_C3D20]
# cell_nodes = [cell_nodes_C3D4, cell_nodes_C3D8, cell_nodes_C3D10, cell_nodes_C3D20]
cell_types = [10, 12, 24, 25]
cell_nodes = [4, 8, 10, 20]

for line in content:
    if line.strip().lower().startswith("*node"):
        flag_node = True
        flag_eles = [False, False, False, False]
        continue
    elif line.strip().lower().startswith("*element"):
        flag_node = False
        flag_eles = [False, False, False, False]
        if "C3D4" in line:
            flag_eles[0] = True
            CELL_TYPE_C3D4 = 10
            cell_nodes_C3D4 = 4
        elif "C3D8" in line:
            flag_eles[1] = True
            CELL_TYPE_C3D8 = 12
            cell_nodes_C3D8 = 8
        elif "C3D10" in line:
            flag_eles[2] = True
            CELL_TYPE_C3D10 = 24
            cell_nodes_C3D10 = 10
        elif "C3D20" in line:
            flag_eles[3] = True
            CELL_TYPE_C3D20 = 25
            cell_nodes_C3D20 = 20
        continue
    elif line.strip().lower().startswith("**"):
        continue
    elif line.strip().lower().startswith("*"):
        flag_node = False
        flag_eles = [False, False, False, False]
        continue
    if flag_node:
        nodes.append(line.strip())
    if flag_eles[0]:
        eles[0].append(line.strip())
    elif flag_eles[1]:
        eles[1].append(line.strip())
    elif flag_eles[2]:
        eles[2].append(line.strip())
    elif flag_eles[3]:
        eles[3].append(line.strip())

f_vtk.write("# vtk DataFile Version 4.2\n")
f_vtk.write("Unstructured Grid Example\n")
f_vtk.write("ASCII\n")
f_vtk.write("DATASET UNSTRUCTURED_GRID\n")
f_vtk.write("POINTS {} double\n".format(len(nodes)))
for node in nodes:
    f_vtk.write("{}\n".format((" ".join(node.split(",")[1:])).strip()))
f_vtk.write("\n")

def write_to_vtk(f, eles, cell_type, cell_nodes):
    eles_ = ",".join(eles)
    eles_ = eles_.replace(" ","")
    eles_ = eles_.replace(",,", ",")
    eles_ = eles_.split(",")
    num_eles = int(len(eles_)/(cell_nodes+1))
    # f.write("CELLS {} {}\n".format(num_eles, len(eles_)))
    CELLS_num = num_eles
    CELLS_total = len(eles_)
    CELLS_content = ""
    CELL_TYPES_content = ""
    for i, v in enumerate(eles_):
        if i%(cell_nodes+1)==0:
            CELLS_content += "{} ".format(cell_nodes)
            # f_vtk.write("{} ".format(cell_nodes))
        else:
            CELLS_content += "{} ".format(int(v)-1)
            # f_vtk.write("{} ".format(int(v)-1))
        if i%(cell_nodes+1)==cell_nodes:
            CELLS_content += "\n"
            # f_vtk.write("\n")
    # f.write("CELL_TYPES {}\n".format(int(len(eles_)/(cell_nodes+1))))
    CELL_TYPES_num = int(len(eles_)/(cell_nodes+1))
    for i in range(num_eles):
        if i%20==19:
            CELL_TYPES_content += "{}\n".format(cell_type)
            # f_vtk.write("{}\n".format(cell_type))
        else:
            CELL_TYPES_content += "{} ".format(cell_type)
            # f_vtk.write("{} ".format(cell_type))
    # f.write("\n")
    CELL_TYPES_content +="\n"

    return CELLS_num, CELLS_total, CELLS_content, CELL_TYPES_num, CELL_TYPES_content


CELLS_num = 0
CELLS_total = 0
CELLS_content = ""

CELL_TYPES_num = 0
CELL_TYPES_content = ""
for i in range(4):
    if eles[i]:
        cells_num, cells_total, cells_content, cell_types_num, cell_types_content = write_to_vtk(f_vtk, eles[i], cell_types[i], cell_nodes[i])
        CELLS_num += cells_num
        CELLS_total += cells_total
        # CELLS_content += cells_content.replace("\n\n", "\n")
        CELLS_content += cells_content
        CELL_TYPES_num += cell_types_num
        # CELL_TYPES_content += cell_types_content.replace("\n\n", "\n")
        CELL_TYPES_content += cell_types_content

f_vtk.write("CELLS {} {}\n".format(CELLS_num, CELLS_total))
f_vtk.write(CELLS_content)
f_vtk.write("CELL_TYPES {}\n".format(CELL_TYPES_num))
f_vtk.write(CELL_TYPES_content)

f_vtk.write("POINT_DATA {}\n".format(len(nodes)))
# f_vtk.write("SCALARS scalars double 1\n")
# f_vtk.write("LOOKUP_TABLE default\n")
# for i in range(len(nodes)):
#     f_vtk.write(str(i)+" ")
#     if i%20 == 19:
#         f_vtk.write("\n")
# f_vtk.write("\n")


f_vtk.close()
