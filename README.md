# surf-trac-to-obj
These scripts are used to generate brain surface and tract files (in .obj format, parcellated and registered) from Freesurfer recon-all and trac-all packages.

## Overview

The surface and tracts imported in Unity:

![](./docs/brain_surf_trac_in_Unity.png)

The complete pial surface read by Mac Preview:

![](./docs/brain_surf_pial.jpeg)

The left-head V1 surface read by Mac Preview:

![](./docs/brain_surf_lh_V1.jpeg)

The left-head Inferior Longitudinal Fasciculus (ILF) with color code RGB-RAS read by Mac Preview:

![](./docs/brain_tract_ilf_colored.jpeg)


## Requirements

- Python 3.x;
- Python packages: numpy, nibabel, Pillow, PyQt5, vispy, pywavefront;
- Prerequisites: Freesurfer 'recon-all' and 'trac-all' result packages prepared.

### Prerequisite steps

Here we list a series of commands (from FSL and Freesurfer) you may need before running **surf2obj** or **trac2obj** scripts. The prerequisite steps should be conducted in a Mac or Linux environment with FSL and Freesurfer installed. If you have those data packages prepared, just skip these steps.

    # run 'recon-all' pipeline; see [Freesurfer](https://surfer.nmr.mgh.harvard.edu/fswiki/recon-all) for more details
    recon-all -i <T1.nii.gz> -s <subid> -all -parallel -openmp 8 ><subid>.log 2>&1

    # convert orig.mgz to nifti format; we will use the recon-all orig space as the standard space as all following images will be registered to it
    mri_convert <$SUBJECTS_DIR/subid/mri/orig.mgz> <$SUBJECTS_DIR/subid/mri/orig.nii.gz>

    # to register the dti image with the orig space before you do 'trac-all' for further convenience and precision; see [FSL flirt&applysfm4d](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FLIRT/UserGuide) for more information
    flirt -in <dwi_raw_b0.nii> -ref <orig.nii.gz> -omat dwi2orig.mat -cost normmi
    applyxfm4d <dwi_raw.nii.gz> <orig.nii.gz> dwi_orig_4d.nii.gz dwi2orig.mat -singlematrix

    # run 'trac-all' pipeline using the registered dwi_orig_4d.nii.gz images; see [Freesurfer trac-all](https://surfer.nmr.mgh.harvard.edu/fswiki/trac-all) for more details
    trac-all -prep -c $TUTORIAL_DATA/diffusion_tutorial/dmrirc.tutorial
    trac-all -bedp -c $TUTORIAL_DATA/diffusion_tutorial/dmrirc.tutorial
    trac-all -path -c $TUTORIAL_DATA/diffusion_tutorial/dmrirc.tutorial

    # you may also want to generate more specific surface labels in the recon-all packages; see [mri_annotation2label](https://surfer.nmr.mgh.harvard.edu/fswiki/mri_annotation2label)
    mri_annotation2label --subject <subif> --hemi <lh/rh> --label <label#int> --outdir <dir> --annotation <'aparc'/'aparc.a2009s'>
    
    # Now you get all result packages ready:) The previous steps may take a long time and you may meet some configuration bugs. Hope you go through it well. Good luck!

## Script Descriptions

- surf2obj.py -- read Freesurfer surface files (.pial, .white, etc.) and write .obj files from them in SurfaceRAS/tkRAS coordinates
- trac2obj.py -- read Freesurfer tract files (.trk) and write .obj files from them in SurfaceRAS/tkRAS coordinates registered with the surface files
