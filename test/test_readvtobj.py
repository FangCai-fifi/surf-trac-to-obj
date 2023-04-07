import os
import re
import random
import numpy as np
import pywavefront

def write_obj(ver, face, objPath, plusOne=True):
    
    if plusOne:
        face1 = 1 + face
    else:
        face1 = np.copy(face)
    
    thefile = open(objPath, 'w')
    
    for item in ver:
        thefile.write("v {0} {1} {2}\n".format(item[0],item[1],item[2]))
    for item in face1:
        thefile.write("f {0} {1} {2}\n".format(item[0],item[1],item[2]))  
        
    thefile.close()

objfile = f"assets/pial.obj"
objfile1 = f"assets/pial_vt.obj"
objdata = pywavefront.Wavefront(objfile, strict=True, encoding="iso-8859-1", parse=False)
objdata.parse()

# print(objdata.vertices.shape)

f1 = open(objfile, 'r')
f2 = open(objfile1, 'a')
lines = f1.readlines()
for line in lines:
    if re.match('f ', line):
        line_ = line.split('\n')[0]
        fnum = line_.split(' ')[1:4]
        f2.write(f"f {fnum[0]}/{random.randint(1, 3220)} {fnum[1]}/{random.randint(1, 3220)} {fnum[2]}/{random.randint(1, 3220)}\n")

f1.close()
f2.close()