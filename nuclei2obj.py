import os
import numpy as np
import nibabel as nib

SUBDIR = 'D:\\neuroimages\\codes\\surfdataset' # replace it with your recon-all package path
SUBNAME = 'hongbo' # replace it with your subject id
NucleiPath = 'D:\\neuroimages\\codes\\surfdataset\\hongbo\\mri\\ThalamicNuclei.v12.T1.mgz'

affine = nib.load(NucleiPath).affine

# write a lh.V1_exvivo.obj
labelPath_rh_lgn = os.path.join(SUBDIR, SUBNAME, 'label', 'rh.lgn.label')
x = np.loadtxt(labelPath_rh_lgn, dtype=None)

ver = x[:, 1:4]
ver_4d = np.hstack((ver, np.ones((ver.shape[0],1))))
print(affine)
print(np.linalg.inv(affine))
ver_vox = np.matmul(np.linalg.inv(affine), np.transpose(ver_4d))
trkvox2tkras = np.array([[-1, 0, 0, 128], [0, 0, -1, 127], [0, 1, 0, -128], [0, 0, 0, 1]]) # LIA
ver_tkras = np.transpose(np.matmul(trkvox2tkras, ver_vox)[0:3, :])

arrLen = ver.shape[0] - 2
face = np.transpose(np.vstack((1 + np.arange(arrLen), 2 + np.arange(arrLen), 3 + np.arange(arrLen))))


objPath = 'assets/hongbo/rh.lgn.obj'
thefile = open(objPath, 'w')
    
for item in ver:
    thefile.write("v {0} {1} {2}\n".format(item[0],item[1],item[2]))
for item in face:
    thefile.write("f {0} {1} {2}\n".format(item[0],item[1],item[2]))  
    
thefile.close()