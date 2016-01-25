# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 15:27:03 2015

@author: prabu
"""

from __future__ import print_function
import sys
import numpy as np
from helpers import closest_array_index


class OutlierDetector:
    
    #------------------------------------------------------------------------
    def __init__(self, zthresh = 1.5, ranges = []):
        self._zthresh = zthresh
        self._ranges = ranges
        self._median = np.array([])
        self._std = np.array([])
    
    
    #------------------------------------------------------------------------
    def detect(self, spectrums):
        
        #check the input is in the right format
        if not isinstance(spectrums, list) or (len(spectrums) < 3):
            print("spectrums must be a list of Spectrum objects")
            sys.exit(0)

        #check wavelengths are same for all spectrums
        w0 = spectrums[0].wavelengths
        if not np.all([np.allclose(w0, s.wavelengths) for s in spectrums]):
            print("spectrums must have same wavelengths")
            sys.exit(0)

            
        #assemble the reflectances in a matrix
        #one row = one spectrum's reflectances
        refls = np.empty((len(spectrums), np.size(w0)), dtype = np.double)
        for (r, s) in enumerate(spectrums):
            refls[r, :] = np.copy(s.reflectances.transpose())

        #find the median spectrum
        median = np.median(refls, axis = 0)

        #compute median of absolute deviations from median
        mad = np.median(np.abs(refls - median), axis = 0)

        #compute robust estimate of standard deviation
        sigma = mad/0.67

        #compute the zscores
        zs = (refls - median)/sigma

        #range indices to look for abnormal deviations        
        rngidxs = []
        for rng in self._ranges:
            start = closest_array_index(rng[0], w0)
            end = closest_array_index(rng[1], w0) + 1
            rngidxs.append(start, end)
        
        #do the outlier detection        
        inliers = []
        outliers = []
        for (specidx, spec) in enumerate(spectrums):
            outlier = False
            for (start, end) in rngidxs:
                if np.any(np.abs(zs[specidx, start:end]) > self._zthresh):
                    outlier = True
            if outlier:
                outliers.append(spec)
            else:
                inliers.append(spec)
        
        #store some stuff in class - useful for plotting
        self._median = median
        self._std = sigma
        
        return (inliers, outliers)


    #------------------------------------------------------------------------    
    @property
    def median(self):
        return self._median

    #------------------------------------------------------------------------        
    @property
    def std(self):
        return self._std

    #------------------------------------------------------------------------
    @property
    def zthresh(self):
        return self._zthresh        


#------------------------------------------------------------------------
if __name__ == "__main__":
    print("OutlierDetector.py")