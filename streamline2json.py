import os
import re
import nibabel as nib
import utils


SUBDIR = '/Users/fangcai/traculaData/diffusion_tutorial/trc' # replace it with your trac-all package path
SUBNAME = 'PZH' # replace it with your subject id
TRKLIST = ['lh.atr', 'lh.cab', 'lh.ccg', 'lh.cst', 'lh.ilf', 'lh.slfp', 'lh.slft', 'lh.unc',
           'rh.atr', 'rh.cab', 'rh.ccg', 'rh.cst', 'rh.ilf', 'rh.slfp', 'rh.slft', 'rh.unc',
           'fmajor', 'fminor']

trkPath = os.path.join(SUBDIR, SUBNAME, 'dpath')
for root, dirs, files in os.walk(trkPath, topdown=True):
    for dirname in dirs:
        for item in TRKLIST:
            if re.search(item, dirname):
                dpath = os.path.join(trkPath, dirname, 'path.pd.trk')
                print(dpath)
                path = nib.streamlines.load(dpath)
                utils.write_streamline_json(path=path, affine=path.affine, jsonpath=f"assets/{item}_traces.json")
