import numpy as np
import nibabel as nib

def read_surf(surfPath):
    
    ver, face = nib.freesurfer.read_geometry(surfPath)
    
    return ver, face


def read_label(labelPath):
    
    label_ver = nib.freesurfer.read_label(labelPath)
    
    return list(label_ver)


def read_parc_surf(ver, face, label_ver):
    
    ver_new = ver[label_ver, :]
    
    face_new = np.array([0, 0, 0])
    for items in face:
        if all(item in label_ver for item in items):
            face_new = np.vstack((face_new, np.array([label_ver.index(items[0]), label_ver.index(items[1]), label_ver.index(items[2])])))
    
    return ver_new, face_new[1:, :]
    

def write_obj(ver, face, objPath, plusOne=True):
    
    if plusOne:
        face1 = 1 + face
    
    thefile = open(objPath, 'w')
    
    for item in ver:
        thefile.write("v {0} {1} {2}\n".format(item[0],item[1],item[2]))
    for item in face1:
        thefile.write("f {0} {1} {2}\n".format(item[0],item[1],item[2]))  
        
    thefile.close()