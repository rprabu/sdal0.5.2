# -*- coding: utf-8 -*-
"""
Created on Mon May  4 00:22:13 2015

@author: prabu
"""

from __future__ import print_function
import numpy as np
from Spectrum import Spectrum


class WaveUniquifier:
    def __init__(self):
        pass
    
    def uniquify(self, spectrum, tol = 0.01):
        diffs = np.diff(spectrum.wavelengths)
        idxs = np.logical_not(diffs < tol)
        idxs = np.hstack((idxs, np.array([True])))
        return Spectrum(data = spectrum.data[idxs],
                        idstr = spectrum.idstr,
                        company = spectrum.company,
                        instrument = spectrum.instrument)
        
        
if __name__ == "__main__":
    print("WaveUniquifier.py")