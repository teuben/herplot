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



ddir = sys.argv[1]

p = get_pacs(ddir + '/level2')
s = get_spire(ddir + '/level2')

print(len(p),len(s))

if len(p) == 0 and len(s) == 0:
    print("No PACS or SPIRE")
elif len(s) > 0 and len(p) == 0:
    print('SPIRE: ',list(s.keys()))
    print('SPIRE: ',s)
    print('SSW: ')
    (ra1,dec1) = get_radec_spire(s['HR_SSW_spectrum2d'])
    print("Pointings: ",len(ra1))
    (hdu1,h1,d1) = get_image(s['HR_SSW_cube'])
    print('SLW: ')
    (ra2,dec2) = get_radec_spire(s['HR_SLW_spectrum2d'])
    print("Pointings: ",len(ra2))
    (hdu2,h2,d2) = get_image(s['HR_SLW_cube'])
    print('# SPIRE')
elif len(p) > 0:
    print('PACS:',list(p.keys()))
    print('PACS:',p)
    r = p['HPS3DEQDR']
    b = p['HPS3DEQIB']
    print('RED:')
    for i in r:
        (hdu,h,d) = get_image(i)
    print('BLUE:')        
    for i in b:
        (hdu,h,d) = get_image(i)
    print('# PACS')        
else:
    print("Should never happen")
        
