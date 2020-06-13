#! /usr/bin/env python
#
#  plot a map or spectrum from a PACS/SPIRE dataset
#  i.e. toying around with the hierarchy of Hershel level2 data

import os
import sys
import glob

import matplotlib
import matplotlib.pyplot as plt

import numpy as np
from astropy.io import fits

ddir = sys.argv[1]

fn0 = glob.glob(ddir + '/*.fits.gz')
print('Found:',fn0)

#    there is only one file, so we can glob this one
hdu0 = fits.open(fn0[0])

h0 = hdu0[2].header
d0 = hdu0[2].data

names = d0['name']
urns  = d0['urn']
ndata = len(names)
for i in range(ndata):
    print(i,names[i],urns[i])

idata = int(sys.argv[2])


fn1 = glob.glob(ddir + '/' + names[idata] + '/*fits.gz')
utype = urns[idata]
print('Found: ',fn1)
print('Type:  ',utype)
hdu1 = fits.open(fn1[0])
print('Found ',len(hdu1),' HDU')

if utype.find('SpectrometerDetectorSpectrum') > 0 or utype.find('SpectrometerPointSourceSpectrum') > 0:
    print('PJT',utype)
    ispec = int(sys.argv[3])
    if ispec < 0:
        print("Header")
        # for each HDU now read the CHNLNAME, RA, DEC,
        for ispec in range(len(hdu1)):
            h1 = hdu1[ispec].header
            d1 = hdu1[ispec].data
            if 'CHNLNAME' in h1:
                nchan = len(d1['wave'])
                w0 = d1['wave'][0]
                w1 = d1['wave'][nchan-1]
                print(ispec,h1['CHNLNAME'],h1['RA'],h1['DEC'],w0,w1,nchan)
            else:
                print(ispec,'-')
                
            
        sys.exit(0)
    h1 = hdu1[ispec].header
    d1 = hdu1[ispec].data
    # assume SPIRE SpectrometerDetectorSpectrum or SpectrometerPointSourceSpectrum
    wave = d1['wave']
    flux = d1['flux']
    ferr = d1['error']
    print(wave.shape)
    print('wave:',wave.min(),wave.max())
    print('flux:',flux.min(),flux.max())
elif utype.find('SlicedPacsCube') > 0:
    # search for the 'bridges' HDU and tell me how many rows it hasn
    h7 = hdu1[7].header
    d7 = hdu1[7].data
    print('Found ',d7.shape[0],' SlicePacsCube')
    fn2 = glob.glob(ddir + '/' + names[idata] + '/herschel.pacs.signal.PacsCube/*fits.gz')
    ispec = int(sys.argv[3])    
    hdu2 = fits.open(fn2[ispec])
    # now grab the 5 x 5 x 22016 cubes
    flux3 = hdu2[1].data
    wave3 = hdu2[2].data
    print('shape:',flux3.shape)
    xpos = int(sys.argv[4])
    ypos = int(sys.argv[5])
    wave = wave3[:,ypos,xpos]
    flux = flux3[:,ypos,xpos]
elif utype.find('SlicedSimpleCube') > 0:
    # herschel.ia.dataset.spectrum.SpectralSimpleCube
    # search for the 'bridges' HDU and tell me how many rows it hasn
    h7 = hdu1[6].header
    d7 = hdu1[6].data
    print('Found ',d7.shape[0],' SlicedSimpleCube')
    fn2 = glob.glob(ddir + '/' + names[idata] + '/herschel.ia.dataset.spectrum.SpectralSimpleCube/*fits.gz')
    print(fn2)
    ispec = int(sys.argv[3])    
    hdu2 = fits.open(fn2[ispec])
    # now grab the 79 x 78 x 135 cube
    # the WCS is in the standard FITS header of HDU1
    head3 = hdu2[1].header
    flux3 = hdu2[1].data
    nspec = flux3.shape[0]
    print("nspec=",nspec)
    xpos = int(sys.argv[4])
    ypos = int(sys.argv[5])
    flux = flux3[:,ypos,xpos]
    wave = np.arange(nspec)    # for now
    print(flux.shape,wave.shape)
elif utype.find('SlicedPacsRebinnedCube') > 0:
    a=0
elif utype.find('SlicedPacsSpecTable') > 0:
    a=0
else:
    print('Dunno this case yet')
    sys.exit(0)



Qscatter = True
Qplot    = True
#
plt.figure()

if Qscatter:
    plt.scatter(wave,flux)
    plt.xlabel('wave (GHz)')
    plt.ylabel('flux W m-2 Hz-1 sr-1')
    plt.ylim([flux.min(),flux.max()])
    plt.title(fn1[0])
if Qplot:    
    plt.plot(wave,flux)
    plt.xlabel('wave (GHz)')
    plt.ylabel('flux W m-2 Hz-1 sr-1')
    plt.ylim([flux.min(),flux.max()])
    plt.title(fn1[0])
    
plt.show()
