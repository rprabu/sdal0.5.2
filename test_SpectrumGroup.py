# -*- coding: utf-8 -*-
"""
Created on Sun May  3 11:47:11 2015

@author: pravindran
"""

from __future__ import print_function
import numpy as np
import os, os.path 
from Spectrum import Spectrum
from SpectrumGroup import SpectrumGroup


def test(testsdir,
         verbose = False):
    idir = os.path.join(testsdir, "input")
    statuses = []
    testcount = 0        
 
    #TEST 1:
    atol = 0.000001   
    testcount = testcount + 1
    #create SpectrumGroup from Spectrum objects
    #--create the Spectrum objects    
    ins = []
    idtmplt = "spec{}"
    company = "csv"
    instrument = "sdal"
    waves = [500.0, 501.0, 502.0, 503.0, 504.0, 505.0, 506.0]
    gstart = 0.1134
    gstep = 0.1
    step = 0.01
    for i in range(4):
        start = gstart + i*gstep
        refls = [(start + j*step) for j in range(len(waves))]
        s = Spectrum(np.array([waves, refls], dtype = np.double).transpose(),
                     idtmplt.format(i+1),
                     company,
                     instrument)
        ins.append(s)
    #--create the SpectrumGroup object
    specgrp = SpectrumGroup(spectrums = ins)
    #--create expected data
    expdata = np.empty((len(ins), len(waves)), dtype = np.double)
    for i in range(4):
        start = gstart + i*gstep
        expdata[i, :] = [(start + j*step) for j in range(len(waves))]
    expwaves = np.array(waves, dtype = np.double)
    expidstrs = [idtmplt.format(i + 1) for i in range(len(ins))]
    expcompanys = [company]*len(ins)
    expinstruments = [instrument]*len(ins)
    #--do the comparisons
    statuses.append(np.allclose(specgrp.data, expdata, atol = atol))   
    statuses.append(np.allclose(specgrp.wavelengths, expwaves, atol = atol))
    statuses.append(specgrp.idstrs == expidstrs)
    statuses.append(specgrp.companys == expcompanys)
    statuses.append(specgrp.instruments == expinstruments)
    if not all(statuses):
        print("Failed TEST {}".format(testcount))
    
    
    #TEST 2:
    testcount = testcount + 1
    #break SpectrumGroup to form Spectrum objects
    outs = specgrp.ungroup()
    for (i, o) in zip(ins, outs):
        statuses.append(i.idstr == o.idstr)
        statuses.append(i.company == o.company)
        statuses.append(i.instrument == o.instrument)
        statuses.append(np.allclose(i.data, o.data, atol = atol))
    if not all(statuses):
        print("Failed TEST {}".format(testcount))
    
    
    #TEST 3:
    testcount = testcount + 1
    #test subsetting
    #--subset
    subgrp = specgrp.wavelength_subset(502.0, 505.0)
    #--create expected data
    expdata = np.array([[ 0.1334, 0.1434, 0.1534, 0.1634],
                        [ 0.2334, 0.2434, 0.2534, 0.2634],
                        [ 0.3334, 0.3434, 0.3534, 0.3634],
                        [ 0.4334, 0.4434, 0.4534, 0.4634]], dtype = np.double)
    expwaves = np.array([502, 503, 504, 505], dtype = np.double)
    #--do comparisons
    statuses.append(np.allclose(subgrp.data, expdata, atol = atol))   
    statuses.append(np.allclose(subgrp.wavelengths, expwaves, atol = atol))
    statuses.append(subgrp.idstrs == expidstrs)
    statuses.append(subgrp.companys == expcompanys)
    statuses.append(subgrp.instruments == expinstruments)
    if not all(statuses):
        print("Failed TEST {}".format(testcount))
        
    
    #TEST 4:
    testcount = testcount + 1
    #test reading from csv and writing to csv
    #--read input.csv    
    ringrp = SpectrumGroup(filename = os.path.join(idir, "input_test4.csv"))
    #--create expected data
    gstart = 0.1134
    gstep = 0.1
    step = 0.01
    expdata = np.empty((4, 7), dtype = np.double)
    for i in range(4):
        start = gstart + i*gstep
        expdata[i, :] = [(start + j*step) for j in range(len(waves))]
    waves = [500.0, 501.0, 502.0, 503.0, 504.0, 505.0, 506.0]
    expwaves = np.array(waves, dtype = np.double)
    expidstrs = ["spec1", "spec2", "spec3", "spec4"]
    expcompanys = ["csv"]*4
    expinstruments = ["sdal"]*4
    #--do the comparisons
    statuses.append(np.allclose(ringrp.data, expdata, atol = atol))   
    statuses.append(np.allclose(ringrp.wavelengths, expwaves, atol = atol))
    statuses.append(ringrp.idstrs == expidstrs)
    statuses.append(ringrp.companys == expcompanys)
    statuses.append(ringrp.instruments == expinstruments)
    if not all(statuses):
        print("Failed TEST {}".format(testcount))
        
    #TEST 5:
    testcount = testcount + 1
    #read input/csv file
    ringrp = SpectrumGroup(filename = os.path.join(idir, "input_test5.csv"))
    #compute stats
    statsgrp = ringrp.compute_stats()
    #ungroup into spectrums
    statspec = statsgrp.ungroup()
    #expected data
    mean = np.array([0.2634, 0.2734, 0.2834, 0.2934, 0.3034, 0.3134, 0.3234], 
                    dtype = np.double)
    std = np.array([0.12909944, 0.12909944, 0.12909944, 0.12909944, 
                    0.12909944, 0.12909944, 0.12909944], dtype = np.double)
    median = np.array([0.2634, 0.2734, 0.2834, 0.2934, 0.3034, 0.3134, 0.3234],
                      dtype = np.double)
    expdata = np.vstack((mean, std, median))
    waves = [500.0, 501.0, 502.0, 503.0, 504.0, 505.0, 506.0]
    expwaves = np.array(waves, dtype = np.double)
    expidstrs = ["sdal_mean", "sdal_std", "sdal_median"]
    expcompany = "asd+csv+tmp"
    expinstrument = "sdal+sdal1+sdal2"
    #do the comparisons
    for (i, s) in enumerate(statspec):
        statuses.append(np.allclose(s.wavelengths, expwaves))
        statuses.append(np.allclose(s.reflectances, expdata[i, :]))
        statuses.append(s.idstr == expidstrs[i])
        statuses.append(s.company == expcompany)
        statuses.append(s.instrument == expinstrument)
    if not all(statuses):
        print("Failed TEST {}".format(testcount))
   
    
    #status message
    if all(statuses):
        print("{}: PASSED".format(__file__))
    else:
        print("{}: FAILED".format(__file__))



if __name__ == "__main__":
    testsdir = "/home/prabu/mycode/sdal/tests_data/test_SpectrumGroup"
    verbose = False
    test(testsdir,
         verbose)