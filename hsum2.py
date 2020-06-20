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
import aplpy

def get_radec_spire(ffile):
    """
    Return a list of (ra,dec) of the pointing in this bintable from the SPIRE data\
    Such files have 17 or 18 columns:
    wave, flux, error, longitude, latitude
    """
    print("get_radec_spire:",ffile)
    hdu = fits.open(ffile)
    print(len(hdu),'luns')
    hdr = hdu[1].header
    dat = hdu[1].data
    if hdr['EXTNAME'] != 'spectrum2d':
        print("Bad EXTNAME = ",hdr['EXTNAME'])
        return None
    ra = dat['longitude']
    dec = dat['latitude']
    waves = hdu[1].data['wave']
    print("wave:",waves.min(),waves.max())
    #fluxs = hdu[1].data['flux']
    return (ra,dec)

def get_radec_pacs(ffile):
    """
    Return a list of (ra,dec) of the pointing in this bintable from the PACS data\
    Such files have 11 columns:
    wave, flux, error, longitude, latitude
    """
    print("get_radec_pacs:",ffile)
    hdu = fits.open(ffile)
    print(len(hdu),'luns')
    hdr = hdu[1].header
    dat = hdu[1].data
    if hdr['EXTNAME'] != 'Spectra':
        print("Bad EXTNAME = ",hdr['EXTNAME'])
        return None
    ra = dat['RightAscension']
    dec = dat['Declination']
    print("Spectra",len(ra))
    waves = hdu[1].data['Wavelength']
    print("Wavelength:",waves.min(),waves.max())
    #fluxs = hdu[1].data['Flux']
    return (ra,dec)

def get_image(ffile):
    """
    return the HDU, Header,Data of an image
    """
    print('get_image:',ffile)
    hdu = fits.open(ffile)
    print(len(hdu),'luns')
    imh = hdu[1].header
    imd = hdu[1].data
    if imh['EXTNAME'] != 'image':
        print("Bad EXTNAME = ",hdr['EXTNAME'])
        return None
    print(imd.shape)
    if len(imd.shape)>2:
        if 'CRVAL3' in imh:
            ch0 = (            1-imh['CRPIX3'])*imh['CDELT3']+imh['CRVAL3']
            chN = (imh['NAXIS3']-imh['CRPIX3'])*imh['CDELT3']+imh['CRVAL3']
            print('Spectral axis:',ch0,chN,imh['CUNIT3'])
        else:
            print("Spectral axis:",imh['CTYPE3'])
    return (hdu[1],imh,imd)

def get_spire(dirname):
    """
    return a dictionary of the fits.gz files from a SPIRE (or PACS) hierarchy one level deep, e.g.
    
    d = get_spire('1342247572/level2')
    gives
    d['HR_SSW_CUBE'] = '1342247572/level2/HR_SSW_cube/hspirespectrometer1342247572_spg_SSW_HR_20ssc_1461672208855.fits.gz'
    """
    fns = glob.glob(dirname + '/*/*.fits.gz')
    d = {}
    for fn in fns:
        fn2 = fn.split('/')
        if fn2[-2] in d:
            print("Multiple entries for",fn2[-2])
        d[fn2[-2]] = fn
    return d

def get_pacs(dirname):
    """
    return a dictionary of the set of fits.gz files from a PACS hierarchy two levels deep, e.g.
    
    unlike get_spire(), this one allows multiple fits files per entry
    """
    fns = glob.glob(dirname + '/*/*/*.fits.gz')
    d = {}
    for fn in fns:
        fn2 = fn.split('/')
        if fn2[-3] in d:
            d[fn2[-3]].append(fn)
        else:
            d[fn2[-3]] = [fn]
    return d


def get_spectrum(ffile,xpos,ypos):
    """
    SPIRE 
    """
    (hdu,h,d) = get_image(ffile)
    sp = d[:,ypos,xpos]
    ch = np.arange(len(sp))
    print("Spectrum min/max",sp.min(),sp.max())
    return (ch,sp)



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
    print("Pointings:",len(ra))
    print("ra:",ra.min(),ra.max())
    print("dec:",dec.min(),dec.max())
    print("wave:",wave.min(),wave.max())
    print("flux:",flux.min(),flux.max()) 
elif extname == 'Spectra':
    # PacsSpecTable:  table of ra,dec,wave,flux; usually two
    # 1342223728/level2/HPSTBRB/herschel.pacs.signal.PacsSpecTable/hpacs1342223728_20hpstbrbs_01_1469458816745.fits.gz 
    ra = d['RightAscension']
    dec = d['Declination']
    print("Spectra",len(ra))
    wave = d['Wavelength']
    flux = d['Flux']
    print("ra:",ra.min(),ra.max())
    print("dec:",dec.min(),dec.max())
    print("wave:",wave.min(),wave.max())
    print("flux:",flux.min(),flux.max()) 
elif extname == 'flux':
    # PascCube, should be a 5 x 5 x Nsample;  there could be 12 of these
    # 1342223728/level2/HPS3DB/herschel.pacs.signal.PacsCube/hpacs1342223728_20hps3dbs_01_1469459163112.fits.gz 
    flux = hdu[1].data
    wave = hdu[2].data
    ra   = hdu[3].data
    dec  = hdu[4].data
    print(ra.shape)
    print("ra:",ra.min(),ra.max())
    print("dec:",dec.min(),dec.max())
    print("wave:",wave.min(),wave.max())
    print("flux:",flux.min(),flux.max()) 
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
