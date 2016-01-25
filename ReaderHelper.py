# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 14:23:06 2015

@author: pravindran
"""

from __future__ import print_function
import numpy as np


class ReaderHelper:
    def __init__(self):
        pass
    
    def read_spectrum_header(self, 
                             filename, 
                             headersep, 
                             datasep = None):
        numskiprows = 0
        wavecol = 0
        reflcol = 1
        hdrdict = {}
        with open(filename) as f:
            datafound = False
            while not datafound:
                #read a line
                l = f.readline()
                #treat the line as data row (i.e all numbers)...
                dstkns = []
                if datasep:
                    dstkns = l.strip().split(datasep)
                else:
                    dstkns = l.strip().split()
                #...try converting the tokens to floats
                status = []
                for t in dstkns:
                    try:
                        #if conversion successful...
                        float(t)
                        status.append(True)
                    except ValueError:
                        #...if conversion not successful
                        status.append(False)
                if all(status):
                    #if all tokens were successfully converted to floats
                    #figure out the wavelength and reflectance column 
                    #numbers based on number of tokens in data line...
                    datafound = True
                    if len(dstkns) == 2:
                        #wavelength, reflectance
                        wavecol = 0
                        reflcol = 1
                    elif len(dstkns) == 3:
                        #index, wavelength, reflectance
                        wavecol = 1
                        reflcol = 2
                    elif len(dstkns) == 4:
                        #wavelength, reference, target, reflectance OR
                        #wavelength, target, reference, reflectance
                        wavecol = 0
                        reflcol = 3
                    elif len(dstkns) == 5:
                        #index, wavelength, reference, target, reflectance OR
                        #index, wavelength, target, reference, reflectance
                        wavecol = 1
                        reflcol = 4
                else:
                    #...conversion of tokens into floats unsuccessful
                    #this is a header line to skip, so keep track
                    numskiprows = numskiprows + 1
                    #...add to header dictionary
                    hstkns = l.strip().split(headersep, 1)
#                    print("hstkns = {}".format(hstkns))
                    if len(hstkns) == 2:
                        hdrdict[hstkns[0].strip()] = hstkns[1].strip()
                    
                    
        return (numskiprows, wavecol, reflcol, hdrdict)

    
    def read_spectrum_data(self, 
                           filename, 
                           numskiprows,
                           wavecol, 
                           reflcol,
                           datasep = None):
        #load in the numerical data
        dm = np.array([])
        if datasep:
            dm = np.loadtxt(filename, 
                            dtype = np.double, 
                            skiprows = numskiprows,
                            delimiter = datasep)
        else:
            dm = np.loadtxt(filename, 
                            dtype = np.double, 
                            skiprows = numskiprows)
        #extract out the wavelength and reflectance columns
        sdm = np.column_stack((dm[:, wavecol], dm[:, reflcol])) 
        #make reflectances in range [0, 1]
        if np.max(sdm[:, 1]) > 1.0:
            sdm[:, 1] = sdm[:, 1]/100.0
        return sdm
    
        
    def uniquefy_wavelengths(self, data):
        #THIS NEEDS TO GO INTO RESAMPLER
        #create dictionaries that hold the unique wavelengths
        #and the order in which they need to go back in
        specdict = {}
        rowdict = {}
        for i in range(np.shape(data)[0]):
            wavestr = str(data[i, 0])
            if wavestr not in specdict:
                rowdict[wavestr] = len(specdict)                
                specdict[wavestr] = data[i, 1]
        #return a new data matrix if needed and return    
        if len(specdict) == np.shape(data)[0]:
            return data
        else:
            newdata = np.empty((len(specdict), 2), dtype = data.dtype)
            for (i, w) in enumerate(specdict):
                row = rowdict[w]
                newdata[row, 0] = float(w)
                newdata[row, 1] = float(specdict[w])
            return newdata
        
        
                                    
        
        
        