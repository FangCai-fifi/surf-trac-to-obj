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
    else:
        face1 = np.copy(face)
    
    thefile = open(objPath, 'w')
    
    for item in ver:
        thefile.write("v {0} {1} {2}\n".format(item[0],item[1],item[2]))
    for item in face1:
        thefile.write("f {0} {1} {2}\n".format(item[0],item[1],item[2]))  
        
    thefile.close()


def read_trk(path):
    tracNum = 0
    verNum = 0
    ver = np.array([0, 0, 0])
    verNum_list = []
    for item in path.streamlines:
        verNum += item.shape[0]
        verNum_list.append(item.shape[0])
        tracNum += 1
        ver = np.vstack((ver, item))
    ver = ver[1:, :]
    
    ver_4d = np.hstack((ver, np.ones((ver.shape[0],1))))
    ver_vox = np.matmul(np.linalg.inv(path.affine), np.transpose(ver_4d))
    trkvox2tkras = np.array([[-1, 0, 0, 128], [0, 1, 0, -128], [0, 0, 1, -127], [0, 0, 0, 1]]) # trk pkg is always LAS orientation!!!
    ver_tkras = np.transpose(np.matmul(trkvox2tkras, ver_vox)[0:3, :])
    
    arrLen = verNum_list[0] - 2
    face = np.transpose(np.vstack((1 + np.arange(arrLen), 2 + np.arange(arrLen), 3 + np.arange(arrLen))))
    arrPre = verNum_list[0]
    for i in range(tracNum-1):
        arrLen = verNum_list[i+1] - 2
        f1 = 1 + arrPre + np.arange(arrLen)
        f2 = 2 + arrPre + np.arange(arrLen)
        f3 = 3 + arrPre + np.arange(arrLen)
        face_tmp = np.transpose(np.vstack((f1, f2, f3)))
        face = np.vstack((face, face_tmp))
        arrPre += verNum_list[i+1]
    
    return ver_tkras, face


def read_trk_lines(path):
    tracNum = 0
    verNum = 0
    ver = np.array([0, 0, 0])
    verNum_list = []
    for item in path.streamlines:
        verNum += item.shape[0]
        verNum_list.append(item.shape[0])
        tracNum += 1
        ver = np.vstack((ver, item))
    ver = ver[1:, :]
    
    ver_4d = np.hstack((ver, np.ones((ver.shape[0],1))))
    ver_vox = np.matmul(np.linalg.inv(path.affine), np.transpose(ver_4d))
    trkvox2tkras = np.array([[-1, 0, 0, 128], [0, 1, 0, -128], [0, 0, 1, -127], [0, 0, 0, 1]]) # trk pkg is always LAS orientation!!!
    ver_tkras = np.transpose(np.matmul(trkvox2tkras, ver_vox)[0:3, :])
    
    lines = {}
    arrLen = verNum_list[0]
    lines[0] = np.arange(1, arrLen, 1)
    arrPre = verNum_list[0]
    for i in range(tracNum-1):
        arrLen = verNum_list[i+1]
        lines[i+1] = np.arange(1+arrPre, arrLen+arrPre, 1)
        arrPre += verNum_list[i+1]
    
    return ver_tkras, lines

def write_obj_line(ver, lines, objPath):
    
    thefile = open(objPath, 'w')
    
    for item in ver:
        thefile.write("v {0} {1} {2}\n".format(item[0],item[1],item[2]))
    for item in lines:
        thefile.write(f"l {' '.join(str(e) for e in lines[item])}\n")
        
    thefile.close()


def write_obj_colored(ver, face, objPath, plusOne=True):
    
    if plusOne:
        face1 = 1 + face
    else:
        face1 = np.copy(face)
    
    thefile = open(objPath, 'w')
    
    for item in ver:
        thefile.write("v {0} {1} {2} {3} {4} {5}\n".format(item[0],item[1],item[2],item[3],item[4],item[5]))
    for item in face1:
        thefile.write("f {0} {1} {2}\n".format(item[0],item[1],item[2]))
        
    thefile.close()


def read_trk_colored(path): # RAS - RGB
    tracNum = 0
    verNum = 0
    ver = np.array([0, 0, 0])
    ver_color = np.array([0, 0, 0])
    verNum_list = []
    for item in path.streamlines:
        verNum += item.shape[0]
        verNum_list.append(item.shape[0])
        tracNum += 1
        ver = np.vstack((ver, item))
        
        delta_xyz = item[2:, :] - item[0:-2, :]
        # print(delta_xyz.shape)
        norm_xyz = np.sqrt(delta_xyz[:, 0] * delta_xyz[:, 0] + delta_xyz[:, 1] * delta_xyz[:, 1] + delta_xyz[:, 2] * delta_xyz[:, 2])
        # print(norm_xyz.shape)
        delta_x = np.true_divide(delta_xyz[:,0], norm_xyz)
        delta_y = np.true_divide(delta_xyz[:,1], norm_xyz)
        delta_z = np.true_divide(delta_xyz[:,2], norm_xyz)
        color_tmp = np.column_stack((delta_x, delta_y, delta_z))
        ver_color = np.vstack((ver_color, np.array([0, 0, 0]), color_tmp, np.array([0, 0, 0])))
        # print(ver_color.shape)
        
    ver = ver[1:, :]
    ver_color = np.abs(ver_color[1:, :])
    
    ver_4d = np.hstack((ver, np.ones((ver.shape[0],1))))
    ver_vox = np.matmul(np.linalg.inv(path.affine), np.transpose(ver_4d))
    trkvox2tkras = np.array([[-1, 0, 0, 128], [0, 1, 0, -128], [0, 0, 1, -127], [0, 0, 0, 1]]) # trk pkg is always LAS orientation!!!
    ver_tkras = np.transpose(np.matmul(trkvox2tkras, ver_vox)[0:3, :])
    
    ver_tkras_color = np.hstack((ver_tkras, ver_color))
    # print(ver_tkras_color.shape)
    
    arrLen = verNum_list[0] - 2
    face = np.transpose(np.vstack((1 + np.arange(arrLen), 2 + np.arange(arrLen), 3 + np.arange(arrLen))))
    arrPre = verNum_list[0]
    for i in range(tracNum-1):
        arrLen = verNum_list[i+1] - 2
        f1 = 1 + arrPre + np.arange(arrLen)
        f2 = 2 + arrPre + np.arange(arrLen)
        f3 = 3 + arrPre + np.arange(arrLen)
        face_tmp = np.transpose(np.vstack((f1, f2, f3)))
        face = np.vstack((face, face_tmp))
        arrPre += verNum_list[i+1]
    
    return ver_tkras_color, face
