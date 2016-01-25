# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 15:13:24 2015

@author: pravindran
"""
from __future__ import print_function
import numpy as np
import math
import sys
from helpers import closest_array_index

class ReferenceDetector:

    def __init__(self, context):
        self._context = context
        self._req_reflectance_range = 0.1
        self._minima_wins = []
        self._minima_radii = []
        if context == "gveg":
            self._req_reflectance_range = 0.25
            self._minima_wins = [(1200.0, 1600.0), 
                                 (1800.0, 2200.0)]
            self._minima_radii = [100.0, 100.0]

        
    def is_reference(self, spectrum):
        refls = spectrum.reflectances
        #if a reflectance is greater than 1.0 then it is a reference
        if np.max(refls) > 1.0:
            return True
            
        if self._context == 'gveg':
            #check the total range of reflectances
            if np.ptp(refls) < self._req_reflectance_range:
                return True
                
            #check presence of minima in specified wavelength ranges
            waves = spectrum.wavelengths
            for (win, rad) in zip(self._minima_wins, self._minima_radii):
                lt_idx = closest_array_index(win[0], waves)
                rt_idx = closest_array_index(win[1], waves)
                minima_found = False
                for i in range(lt_idx, rt_idx):
                    cval = refls[i]
                    li = max(i - rad, 0)
                    ri = min(i + rad, len(refls))
                    if np.all(np.greater_equal(refls[li:ri], cval)):
                        minima_found = True
                if not minima_found:
                    return True
                    
        return False

#        
#        #test based in 'features'
#        statuses = []
#        refls = spectrum.reflectances
#        reflrange = np.amax(refls) - np.amin(refls)
#        statuses.append(reflrange >= self._req_reflectance_range)
#        for i in range(len(self._minima_wins)):
#            statuses.append(self._minima_test(spectrum,
#                                              self._minima_wins[i], 
#                                              self._minima_radii[i]))
#        return not all(statuses)
        
        
#    def _minima_test(self, spectrum, locwin, radius):
#        print("locwin = {}".format(locwin))
#        waves = spectrum.wavelengths
#        refls = spectrum.reflectances    
#        idx1 = closest_array_index(locwin[0], waves)
#        idx2 = closest_array_index(locwin[1], waves)
#        minidx = -1
#        for i in range(idx1, idx2):
#            cval = refls[i]
#            ileft = max(i - radius, 0)
#            iright = min(i + radius, len(refls))
#            if np.all(np.greater_equal(refls[ileft:iright], cval)):
#                minidx = i
#        return (minidx > 0)
        
#        
#    def do_detection(self, spectrums):
#        if self._context == "gveg":
#            if isinstance(spectrums, list):
#                for s in spectrums:
#                    self._detect_gveg(s)
#            else:
#                self._detect_gveg(spectrums)
#    
#    def _detect_gveg(self, s):
#        reflectances = s.reflectances
#        rangetest = self._range_test(reflectances, 
#                                     self._gveg_min_range)
#        min1test = self._minima_test(reflectances, 
#                                     s.w2i(self._gveg_minima1_loc),
#                                     self._gveg_minima_radius)
#        min2test = self._minima_test(reflectances, 
#                                     s.w2i(self._gveg_minima2_loc),
#                                     self._gveg_minima_radius)
#        s.is_reference = not np.all([rangetest, min1test, min2test])
#                                         
#                
#    def _range_test(self, reflectances, reqrange):
#        refrange = np.amax(reflectances) - np.amin(reflectances)
#        return (refrange >= reqrange)
#
#        
#    def _minima_test(self, reflectances, idxrange, idxradius):
#        minidx = -1
#        for i in range(idxrange[0], idxrange[1]):
#            cval = reflectances[i]
#            ileft = max(i - idxradius, 0)
#            iright = min(i + idxradius, len(reflectances))
#            if np.all(np.greater_equal(reflectances[ileft:iright], cval)):
#                minidx = i
#        print("minidx = {}".format(minidx))
#        return (minidx > 0)
    
if __name__ == "__main__":
    print("SpectrumReferenceDetector.py")
    

