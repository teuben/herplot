# herplot

Some simple plotting in Hershel level2 data using python3

## Hershel (2009-2013)

There were 3 instruments on Hershel

* HIFI (S: single pixel  157 to 625 um or 480-1910 GHz)  - 7 bands [R=1e6-1e7])
* PACS (I: 70, 100, 160   P: 194-672 um    + S:  55-210 um (R=1000-5000))
* SPIRE (P: 250, 350, 500 um + FTS:  194-318 um and 294-671 um [R=20-1000])

For the purpose of the range of things were are doing here, we only look at SPIRE and PACS

### SPIRE photometry


### SPIRE spectra


The short 194-318 um (944-1568 GHz) is labeled "SS".  E.g. SSWA1 , they refer to a position on the sky
The long  294-671 um (446-1017 GHz) is labeled "SL".  E.g  SLWC4


            SpectrometerDetectorSpectrum     SpectrometerPointSourceSpectrum        numChans
      SL           19 positions                       7                               1905
      SS           35                                17                               2082
     units       ~1e-19                              ~1



### PACS

## Links

* https://www.cosmos.esa.int/web/herschel
* https://www.cosmos.esa.int/web/herschel/data-products-overview
* HSA: http://archives.esac.esa.int/hsa/whsa/
* https://www.cosmos.esa.int/web/herschel/user-contributed-software
* anything in pySpeckit ?
