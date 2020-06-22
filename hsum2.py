#! /usr/bin/env python3
#
#  summarize a PACS or SPIRE spectral dataset
#
import os
import sys
import glob

import matplotlib
import matplotlib.pyplot as plt

import numpy as np
from astropy.io import fits


ffile = sys.argv[1]


hdu = fits.open(ffile)
print(len(hdu),'luns')
h = hdu[1].header
d = hdu[1].data
extname = h['EXTNAME']
if extname == 'spectrum2d':
    # SpireSpectroPoint: table or ra,dec,wave,flux
    # 1342247572/level2/HR_SLW_spectrum2d/hspirespectrometer1342247572_spg_SLW_HR_20spc_1461672208029.fits.gz
    ra = d['longitude']
    dec = d['latitude']
    wave = d['wave']
    flux = d['flux']
    n = len(ra)
    print("# Pointings:",n)
    print("# ra:",ra.min(),ra.max())
    print("# dec:",dec.min(),dec.max())
    print("# wave:",wave.min(),wave.max())
    print("# flux:",flux.min(),flux.max())
    for i in range(n):
        print(ra[i],dec[i])
    
elif extname == 'Spectra':
    # PacsSpecTable:  table of Spectra ra,dec,wave,flux; usually two
    # 1342223728/level2/HPSTBRB/herschel.pacs.signal.PacsSpecTable/hpacs1342223728_20hpstbrbs_01_1469458816745.fits.gz 
    ra = d['RightAscension']
    dec = d['Declination']
    print("Spectra",len(ra))
    wave = d['Wavelength']
    flux = d['Flux']
    n = len(ra)
    print("# ra:",ra.min(),ra.max())
    print("# dec:",dec.min(),dec.max())
    print("# wave:",wave.min(),wave.max())
    print("# flux:",flux.min(),flux.max())
    for i in range(n):
        print(wave[i],flux[i],ra[i],dec[i])
elif extname == 'flux':
    # PascCube, should be a 5 x 5 x Nsample;  there could be 12 of these
    # 1342223728/level2/HPS3DB/herschel.pacs.signal.PacsCube/hpacs1342223728_20hps3dbs_01_1469459163112.fits.gz 
    flux = hdu[1].data
    wave = hdu[2].data
    ra   = hdu[3].data
    dec  = hdu[4].data
    n = ra.shape[0]
    print(ra.shape,n)
    print("# ra:",ra.min(),ra.max())
    print("# dec:",dec.min(),dec.max())
    print("# wave:",wave.min(),wave.max())
    print("# flux:",flux.min(),flux.max())
    for i in range(n):
        for j in range(5):
            for k in range(5):
                print(wave[i,j,k],flux[i,j,k],ra[i,j,k],dec[i,j,k])
else:
    print("Unknown extension ",h['EXTNAME'])


# Sample output
"""
./hsum2.py 1342223728/level2/HPSTBRB/herschel.pacs.signal.PacsSpecTable/hpacs1342223728_20hpstbrbs_01_1469458816745.fits.gz 
6 luns
Spectra 34000
ra: 185.7380811067591 185.75392976212555
dec: 15.819052554992595 15.833975876180002
wave: 78.5002105041251 80.13596726629902
flux: nan nan

./hsum2.py 1342223728/level2/HPS3DB/herschel.pacs.signal.PacsCube/hpacs1342223728_20hps3dbs_01_1469459163112.fits.gz 
25 luns
(48000, 5, 5)
ra: 185.7380727207353 185.75273819178975
dec: 15.81900407812371 15.832839123513672
wave: 88.23748331195871 89.44039193901743
flux: nan nan

./hsum2.py 1342247572/level2/HR_SLW_spectrum2d/hspirespectrometer1342247572_spg_SLW_HR_20spc_1461672208029.fits.gz
2 luns
Pointings: 76
ra: 185.69256686799983 185.75403196518687
dec: 15.790527782209395 15.852941845618396
wave: 446.99055488 1017.79539491
flux: -1.2665450564010296e-18 1.5479552620358425e-18

"""
