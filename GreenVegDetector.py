# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 11:00:20 2015

@author: pravindran
"""

from __future__ import print_function
import numpy as np
from helpers import closest_array_index

class GreenVegDetector:
    
    #-------------------------------------------------------------
    def __init__(self, 
                 ndvi_thresh = 0.5,
                 ndvi_nir_range = (800, 850),
                 ndvi_red_range = (635, 685),
                 reflectance_range_thresh = 0.25):
        self._ndvi = 0.0
        self._reflectance_range = 0.0
        self._ndvi_thresh = ndvi_thresh
        self._ndvi_nir_range = ndvi_nir_range
        self._ndvi_red_range = ndvi_red_range
        self._reflectance_range_thresh = reflectance_range_thresh
        
        
    #-------------------------------------------------------------
    def is_green_vegetation(self, spectrum):
        self._ndvi, self._reflectance_range = 0.0, 0.0
        waves = spectrum.wavelengths
        refls = spectrum.reflectances
        
        #perform the ndvi based test
        nir_start = closest_array_index(self._ndvi_nir_range[0], waves)
        nir_end = closest_array_index(self._ndvi_nir_range[1], waves)
        red_start = closest_array_index(self._ndvi_red_range[0], waves)
        red_end = closest_array_index(self._ndvi_red_range[1], waves)
        nir_mean = np.mean(refls[nir_start:nir_end])
        red_mean = np.mean(refls[red_start:red_end])
        self._ndvi = (nir_mean - red_mean)/(nir_mean + red_mean) 
        if self._ndvi < self._ndvi_thresh:
            return (False, self._ndvi, self._reflectance_range)
        
        #perform reflectance range based test
        #consider the middle 90% of wavelengths
        chop_size = np.size(refls)*5/100 + 1
        start = chop_size
        stop = np.size(refls) - chop_size
        self._reflectance_range = np.ptp(refls[start:stop])
        if self._reflectance_range < self._reflectance_range_thresh:
            return (False, self._ndvi, self._reflectance_range)
        
        #it is green vegetation if this point is reached
        return (True, self._ndvi, self._reflectance_range)
    
    
    #-------------------------------------------------------------
    @property
    def ndvi(self):
        return self._ndvi
    
    
    #-------------------------------------------------------------
    @property
    def reflectance_range(self):
        return self._reflectance_range
    
    
    #-------------------------------------------------------------
    @property
    def ndvi_nir_range(self):
        return self._ndvi_nir_range
    
    
    #-------------------------------------------------------------
    @property
    def ndvi_red_range(self):
        return self._ndvi_red_range
    

    #-------------------------------------------------------------
    @property
    def ndvi_thresh(self):
        return self._ndvi_thresh
    
    
    #-------------------------------------------------------------
    @property
    def reflectance_range_thresh(self):
        return self._reflectance_range_thresh
        


#-------------------------------------------------------------
if __name__ == "__main__":
    print("GreenVegDetector.py")