import os
import numpy as np
import utils

SUBDIR = '/Applications/freesurfer/7.1.0/subjects'
SUBNAME = 'PZH'


# lh.pial to lh.pial.obj
surfPath_lh_pial = os.path.join(SUBDIR, SUBNAME, 'surf', 'lh.pial')
verl, facel = utils.read_surf(surfPath=surfPath_lh_pial)
utils.write_obj(ver=verl, face=facel, objPath='assets/lh.pial.obj', plusOne=True)


# rh.pial to rh.pial.obj
surfPath_rh_pial = os.path.join(SUBDIR, SUBNAME, 'surf', 'rh.pial')
verr, facer = utils.read_surf(surfPath=surfPath_rh_pial)
utils.write_obj(ver=verr, face=facer, objPath='assets/rh.pial.obj', plusOne=True)


# write a combined pial.obj
all_ver = np.concatenate([verl, verr], axis=0)
tmp_facer = facer + verl.shape[0]
all_face = np.concatenate([facel, tmp_facer], axis=0)
utils.write_obj(ver=all_ver, face=all_face, objPath='assets/pial.obj', plusOne=True)


# write a lh.V1_exvivo.obj
labelPath_lh_V1 = os.path.join(SUBDIR, SUBNAME, 'label', 'lh.V1_exvivo.label')
label_ver_lh_V1 = utils.read_label(labelPath=labelPath_lh_V1)
ver_lh_V1, face_lh_V1 = utils.read_parc_surf(ver=verl, face=facel, label_ver=label_ver_lh_V1)
utils.write_obj(ver=ver_lh_V1, face=face_lh_V1, objPath='assets/lh.V1_exvivo.obj', plusOne=True)

# write an rh.MT_exvivo.obj
labelPath_rh_MT = os.path.join(SUBDIR, SUBNAME, 'label', 'rh.MT_exvivo.label')
label_ver_rh_MT = utils.read_label(labelPath=labelPath_rh_MT)
ver_rh_MT, face_rh_MT = utils.read_parc_surf(ver=all_ver, face=all_face, label_ver=label_ver_rh_MT)
utils.write_obj(ver=ver_rh_MT, face=face_rh_MT, objPath='assets/rh.MT_exvivo.obj', plusOne=True)