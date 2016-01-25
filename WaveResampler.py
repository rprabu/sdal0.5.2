# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 13:08:55 2015

@author: pravindran
"""

from __future__ import print_function
import sys
import math
import numpy as np
from scipy.interpolate import interp1d
from Spectrum import Spectrum
from ChsInterpolator import ChsInterpolator


class WaveResampler:
    """
    A class that resamples to produce integer wavelengths.
    Resampling is done so that the integer wavelengths are strictly 
    within input wavelength range. Options are linear interpolation 
    (using scipy) and cubic hermite spline interpolation (using 
    Prabu's implementation). For each input spectrum, a new resampled 
    spectrum object is returned. 
    
    Sample usage:
    ------------
    #for linear interpolation 
    resampler = WaveResampler(rstype = 'linear')
    rs = resampler(s)
    #for cubic interpolation
    resampler = WaveResampler(rstype = 'cubic')
    rs = resampler(s)
    
    Sample usage notes:
    ------------------
    #rs = resampled spectrum
    #s = spectrum
    """

    def __init__(self, rstype = 'linear', 
                 wavestart = 350.0, 
                 wavestop = 2500.0,
                 spacing = 1.0):
        self._resampletype = rstype
        self._wavestart = wavestart
        self._wavestop = wavestop
        self._spacing = spacing


    def resample(self, spectrum):
        #make local copies to aid readability
        waves = spectrum.wavelengths
        refls = spectrum.reflectances
        if self._wavestart < waves[0] or self._wavestop > waves[-1]:
            print("WaveResampler: Trying to resample out of range")
            spectmplt = "Spectrum wavelength range: {} to {}" 
            print(spectmplt.format(waves[0], waves[-1]))
            reqtmplt = "Specified wavelength range: {} to {}"
            print(reqtmplt.format(self._wavestart, self._wavestop))
            sys.exit(0)
        wstart = self._wavestart
        wstop = self._wavestop
        numsamples = int((wstop - wstart)/self._spacing) + 1
        rswaves = np.linspace(wstart, wstop, numsamples)
        rsrefls = np.array([])
        if self._resampletype == "linear":
            #get the interpolation fit
            inrefls = interp1d(waves, refls, kind = self._resampletype)
            #do resampling at resampled wavelengths
            rsrefls = inrefls(rswaves)
        elif self._resampletype == "cubic":
            spliner = ChsInterpolator()
            #get the interpolation fit
            spliner.fit(waves, refls)
            #do resampling at resampled wavelengths
            rsrefls = spliner.predict(rswaves)
            pass
        else:
            tmplt = "{} Unknown resampling type {}" 
            print(tmplt.format(__file__, self._resampletype))
            sys.exit(0)
        return Spectrum(data = np.column_stack((rswaves, rsrefls)),
                        idstr = spectrum.idstr,
                        company = spectrum.company,
                        instrument = spectrum.instrument,
                        metadata = spectrum.metadata())
                
if __name__ == "__main__":
    print("WaveResampler.py")
