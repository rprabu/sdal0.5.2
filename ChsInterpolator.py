# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 13:48:57 2015

@author: pravindran
"""

from __future__ import print_function
import numpy as np

class ChsInterpolator:
    """
    A class that performs cubic Hermite spline interpolation.
    The api for this class are the functions learn() and predict().
    The arguments to and returns from these functions are numpy arrays. 
    """
    def __init__(self):
        self._tlearn = None
        self._plearn = None

    
    def fit(self, tlearn, plearn):
        #make local copies
        self._tlearn = np.copy(tlearn)
        self._plearn = np.copy(plearn)
        #find the slopes
        tfwd = np.roll(self._tlearn, -1) - self._tlearn
        tbwd = np.roll(tfwd, 1)
        pfwd = np.roll(self._plearn, -1) - self._plearn
        pbwd = np.roll(pfwd, 1)
        self._slopes = pfwd/(2.0*tfwd) + pbwd/(2.0*tbwd)
        self._slopes[0] = pfwd[0]/tfwd[0]
        self._slopes[-1] = pbwd[-1]/tbwd[-1]
        
        
    def predict(self, tpredict):
        ridxs = np.searchsorted(self._tlearn, tpredict)
#        print("ridxs = {}".format(ridxs))
#        print("len(self._tlearn) = {}".format(len(self._tlearn)))
        if np.any( np.logical_or(ridxs < 1, ridxs >= len(self._tlearn)) ):
            print("ERROR:Prediction outside learning range expected")
            return np.array([])
        lidxs = ridxs - 1
        t = ((tpredict - self._tlearn[lidxs])/
                (self._tlearn[ridxs] - self._tlearn[lidxs]))
        t2 = np.power(t, 2)
        t3 = np.power(t, 3)
        twdt = self._tlearn[ridxs] - self._tlearn[lidxs]
        h00 = 2*t3 - 3*t2 + 1
        h10 = t3 - 2*t2 + t
        h01 = -2.0*t3 + 3.0*t2
        h11 = t3 - t2
        return (h00*self._plearn[lidxs] + h10*twdt*self._slopes[lidxs] + 
                h01*self._plearn[ridxs] + h11*twdt*self._slopes[ridxs])
    
    
if __name__ == "__main__":
    print("CubicHermiteSplineInterpolator")
    