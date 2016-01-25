# -*- coding: utf-8 -*-
"""
Created on Sun May  3 23:27:29 2015

@author: prabu
"""

from __future__ import print_function
import os, os.path
import numpy as np
from SdalReader import SdalReader
from WaveUniquifier import WaveUniquifier
from WaveResampler import WaveResampler

def test(testsdir, verbose = False):
    idir = os.path.join(testsdir, "input")
    edir = os.path.join(testsdir, "expect")
    statuses = []
    
    #TEST 1:
    #resampling sig data
    #--create filenames
    ifs = ["input_sig_test1.sig",
           "input_sig_test2.sig",
           "input_sig_test3.sig"]
    ifs = [os.path.join(idir, f) for f in ifs]
    efs = ["expect_sig_test1.sig",
           "expect_sig_test2.sig",
           "expect_sig_test3.sig"]
    efs = [os.path.join(edir, f) for f in efs]
    #--load the spectrums
    ins = [SdalReader().read_spectrum(f) for f in ifs]
    uniquifier = WaveUniquifier()
    ins = [uniquifier.uniquify(s) for s in ins]
    exs = [SdalReader().read_spectrum(f) for f in efs]
    #--resample the input spectrums
    wavestart = 350.0
    wavestop = 2500.0
    resampler = WaveResampler(rstype = "linear",
                              wavestart = wavestart,
                              wavestop = wavestop,
                              spacing = 1.0)
    inrs = [resampler.resample(s) for s in ins]
    #--subset input resampled and expect spectrums
    subexs = [s.wavelength_subset(wavestart, wavestop) for s in exs]
    #--do the comparisons
    testcount = 0
    for (si, se) in zip(inrs, subexs):
        testcount = testcount + 1
        statuses.append(np.allclose(si.data, se.data, atol = 0.001))
        if not all(statuses):
            print("Failed TEST 1-{}".format(testcount))
    
    #TEST 2:
    #resampling sed data
    #--create filenames
    ifs = ["input_sed_test1.sed",
           "input_sed_test2.sed",
           "input_sed_test3.sed"]
    ifs = [os.path.join(idir, f) for f in ifs]
    efs = ["expect_sed_test1.sed",
           "expect_sed_test2.sed",
           "expect_sed_test3.sed"]
    efs = [os.path.join(edir, f) for f in efs]
    #--load the spectrums
    ins = [SdalReader().read_spectrum(f) for f in ifs]
    uniquifier = WaveUniquifier()
    ins = [uniquifier.uniquify(s) for s in ins]
    exs = [SdalReader().read_spectrum(f) for f in efs]
    #--resample the input spectrums
    wavestart = 350.0
    wavestop = 2500.0
    resampler = WaveResampler(rstype = "cubic",
                              wavestart = wavestart,
                              wavestop = wavestop,
                              spacing = 1.0)
    inrs = [resampler.resample(s) for s in ins]
    #--subset input resampled and expect spectrums
    subexs = [s.wavelength_subset(wavestart, wavestop) for s in exs]
    #--do the comparisons
    testcount = 0
    for (si, se) in zip(inrs, subexs):
        testcount = testcount + 1
        statuses.append(np.allclose(si.data, se.data, atol = 0.01))
        if not all(statuses):
            print("Failed TEST 2-{}".format(testcount))
    
    #TEST : 3
    #resampling sig data
    #--create filenames
    ifs = ["input_sig_test1.sig",
           "input_sig_test2.sig",
           "input_sig_test3.sig"]
    ifs = [os.path.join(idir, f) for f in ifs]
    #--load the spectrums
    ins = [SdalReader().read_spectrum(f) for f in ifs]
    uniquifier = WaveUniquifier()
    ins = [uniquifier.uniquify(s) for s in ins]
    #--resample the input spectrums
    resampler = WaveResampler(rstype = "linear", 
                              wavestart = 338.0,
                              wavestop = 2500.0,
                              spacing = 2.0)
    inrs = [resampler.resample(s) for s in ins]

    #status message
    if all(statuses):
        print("{}: PASSED".format(__file__))
    else:
        print("{}: FAILED".format(__file__))
        
        
if __name__ == "__main__":
    testsdir = "/home/prabu/mycode/sdal/tests_data/test_WaveResampler"
    verbose = False
    test(testsdir, verbose)
    