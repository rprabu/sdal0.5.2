# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 14:02:08 2015

@author: prabu
"""

from __future__ import print_function
import math
import numpy as np
from Spectrum import Spectrum
from WaveUniquifier import WaveUniquifier
from WaveResampler import WaveResampler
from helpers import closest_array_index

class OverlapHandler:
    
    #-------------------------------------------------------------------------
    def __init__(self, rstype = 'linear'):
        self._rstype = rstype

    def is_1nm(self, spectrum):
        diffs = np.diff(spectrum.wavelengths)
        return np.allclose(diffs, np.repeat(1.0, np.size(diffs)))
    
    
    #-------------------------------------------------------------------------    
    def process_overlap(self, spec):
        #find the forward difference for the wavelengths
        diffs = np.diff(spec.wavelengths)
        #find where the wavelength differences are negative
        idxs = np.nonzero(diffs <= -0.05)[0]
        idxs = idxs + 1
        idxs = np.hstack((np.array([0]), idxs, np.size(spec.wavelengths)))
        #create pieces os spectrums with increasing wavelengths
        pcs = []
        data = spec.data
        uniquifier = WaveUniquifier()
        for k in range(1, len(idxs)):
            i1 = idxs[k - 1]
            i2 = idxs[k]
            s = Spectrum(data = data[i1:i2, :],
                         idstr = spec.idstr,
                         company = spec.company,
                         instrument = spec.instrument)
            pcs.append(uniquifier.uniquify(s))
        #resample the pieces into 1 nm wavelengths
        rspcs = []
        resampler = WaveResampler()
        for s in pcs:
            wr = s.wavelength_range()
            start = math.ceil(wr[0])
            stop = math.floor(wr[1])
            resampler = WaveResampler(rstype = self._rstype,
                                      wavestart = start,
                                      wavestop = stop,
                                      spacing = 1.0)
            rspcs.append(resampler.resample(s))
#            print(rspcs[-1].wavelengths[0], rspcs[-1].wavelengths[-1])
#        print("------------------------")

        
        #chop and stitch
        if len(rspcs) > 1:
            #find the wavelengths to chop at
            critwaves = [rspcs[0].wavelengths[0]]
            for i in range(1, len(rspcs)):
                #find the overlapping indices
                lstart, lstop, rstart, rstop = -1, -1, -1, -1
                rstart = 0
                lstart = closest_array_index(rspcs[i].wavelengths[0],
                                             rspcs[i - 1].wavelengths)
                lstop = len(rspcs[i - 1].wavelengths)
                rstop = closest_array_index(rspcs[i - 1].wavelengths[-1], 
                                            rspcs[i].wavelengths) + 1
                lrefls = rspcs[i - 1].reflectances[lstart:lstop]
                rrefls = rspcs[i].reflectances[rstart:rstop]
                lwaves = rspcs[i - 1].wavelengths[lstart:lstop]
                critwaves.append(lwaves[np.argmin(np.abs(lrefls - rrefls))])
            critwaves.append(rspcs[-1].wavelengths[-1])
#            print("critwaves = {}".format(critwaves))
            subdms = []
            for i in range(len(rspcs)):
                start = closest_array_index(critwaves[i], 
                                            rspcs[i].wavelengths)
                stop = closest_array_index(critwaves[i + 1],
                                           rspcs[i].wavelengths) + 1
                subdms.append(rspcs[i].data[start:stop, :])
#                print(rspcs[i].data[start:stop, :])
#            print("========================")
            return uniquifier.uniquify(Spectrum(data = np.vstack(tuple(subdms)),
                            idstr = spec.idstr,
                            company = spec.company,
                            instrument = spec.instrument))
        else:
            return rspcs[0]
        

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------    
if __name__ == "__main__":
    print("OverlapHandler.py")
    
    