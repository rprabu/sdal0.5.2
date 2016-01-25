# -*- coding: utf-8 -*-
"""
Created on Thu May 21 19:39:30 2015

@author: prabu
"""

from __future__ import print_function
import numpy as np
from Spectrum import Spectrum
from helpers import closest_array_index

class JumpCorrector:
    
    def __init__(self,
                 jumpwavelengths,
                 stablezone):
        self._jumpwaves = jumpwavelengths
        self._stablezone = stablezone
        self._dm = np.empty([], dtype = np.double)

    
    def correct(self, spectrum):
        self._dm = np.copy(spectrum.data)
        self._correct_postzones()
        self._correct_prezones()
        return Spectrum(data = self._dm,
                        idstr = spectrum.idstr,
                        company = spectrum.company,
                        instrument = spectrum.instrument)
        
        
    def _correct_prezones(self):
        zones = range(self._stablezone - 1, -1, -1)
        for z in zones:
            ix = closest_array_index(self._jumpwaves[z], self._dm[:, 0])
            sjump = self._dm[ix, 1] - self._dm[(ix + 1), 1]
            ujump = self._dm[(ix - 2), 1] - self._dm[(ix - 1), 1]
            avjump = (sjump + ujump)/2.0
            scale = (self._dm[ix, 1] + avjump)/self._dm[(ix - 1), 1]
            self._dm[0:ix, 1] = self._dm[0:ix, 1]*scale 
    
    
    def _correct_postzones(self):
        zones = range(self._stablezone + 1, len(self._jumpwaves) + 1)
        for z in zones:
            ix = closest_array_index(self._jumpwaves[z - 1], self._dm[:, 0])
            sjump = self._dm[ix, 1] - self._dm[(ix - 1), 1]
            ujump = self._dm[(ix + 2), 1] - self._dm[(ix + 1), 1]
            avjump = (sjump + ujump)/2.0
            scale = (self._dm[ix, 1] + avjump)/self._dm[(ix + 1), 1]
            self._dm[(ix + 1):, 1] = self._dm[(ix + 1):, 1]*scale 


if __name__ == "__main__":
    print("JumpCorrector.py")