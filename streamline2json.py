import os
import json
import numpy as np
import nibabel as nib
import utils

path = nib.streamlines.load('assets/path.pd.trk')
affine = path.affine
Trkvox2tkras = np.array([[-1, 0, 0, 128], [0, 1, 0, -128], [0, 0, 1, -127], [0, 0, 0, 1]]) # trk pkg is always LAS orientation!!!


verNum_list = []
for item in path.streamlines:
    verNum_list.append(item.shape[0])

frameNum = max(verNum_list)
max_index = verNum_list.index(frameNum)

frames = {}
line = path.streamlines[0]
ver_tkras = utils.ras2tkras(ver=line, affine=affine, trkvox2tkras=Trkvox2tkras)

for i in range(frameNum):
    if i < verNum_list[0]:
        frames[i] = list(ver_tkras[i, :])
    else:
        frames[i] = list(ver_tkras[-1, :])

j = 1
for item in path.streamlines[1:]:
    ver_tkras = utils.ras2tkras(ver=item, affine=affine, trkvox2tkras=Trkvox2tkras)

    # write frames in json
    for i in range(frameNum):
        if i < verNum_list[j]:
            frames[i] += (list(ver_tkras[i, :]))
        else:
            frames[i] += (list(ver_tkras[-1, :]))
    
    j += 1


with open("assets/traces.json", "w") as outfile:
    json.dump(frames, outfile)