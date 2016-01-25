# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 23:22:50 2015

@author: prabu
"""

from __future__ import print_function
import os, os.path
import math
from WaveResampler import WaveResampler
from PicoReader import PicoReader

class PicoProcessor:
    def __init__(self,
                 interpolation = 'linear'):
        self._interpolation = interpolation
    
    def process(self, spectrum_list):
        proc_list = []
        for s in spectrum_list:
            wr = WaveResampler(rstype = self._interpolation,
                               wavestart = float(math.ceil(s.wavelengths[0])), 
                               wavestop = float(math.floor(s.wavelengths[-1])),
                               spacing = 1.0)
            proc_list.append(wr.resample(s))
        return proc_list
    
    

if __name__ == "__main__":
    print("PicoProcessor.py")
    
    d = '/home/prabu/mycode/sdal_data/tests_data/pico_test1/'
#    f = os.path.join(d, '000001_v1_multiplespectrometers.pico')
    f = os.path.join(d, '000007_v1_multiplespectrometers_no_dark.pico')
    
    pr = PicoReader()
    orig_spectrums = pr.read(f)
    print(orig_spectrums[0].metadata())  
    print(orig_spectrums[0].data)
    print("------------------------")
    
    pp = PicoProcessor()
    proc_spectrums = pp.process(orig_spectrums)
    print(proc_spectrums[0].metadata())
    print(proc_spectrums[0].data)
    print(proc_spectrums[1].data)