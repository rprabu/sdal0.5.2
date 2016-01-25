# -*- coding: utf-8 -*-
"""
Created on Sat May  2 21:49:41 2015

@author: pravindran
"""

from __future__ import print_function
import numpy as np
import os, os.path
from Spectrum import Spectrum


def test(testsdir,
         verbose = False):
    edir = os.path.join(testsdir, "expect")
    odir = os.path.join(testsdir, "output")
    statuses = []
    testcount = 0

    
    #TEST 1:
    testcount = testcount + 1
    #test if we can create a Spectrum object
    #this also tests the properties
    dm = np.array([[340, 0.1234], [341, 0.2234], [342, 0.3234], 
                   [343, 0.4234], [344, 0.5234], [345, 0.6234]], 
                   dtype = np.double)
    idstr = "test"
    company = "csv"
    instrument = "csv"
    s = Spectrum(dm, idstr, company, instrument)
    expwaves = np.array([340, 341, 342, 343, 344, 345], 
                        dtype = np.double)
    exprefls = np.array([0.1234, 0.2234, 0.3234, 0.4234, 0.5234, 0.6234], 
                        dtype = np.double)
    statuses.append(np.array_equal(s.wavelengths, expwaves))
    statuses.append(np.array_equal(s.reflectances, exprefls))
    if not all(statuses):
        print("Failed TEST {}".format(testcount))
    
    #TEST 2
    testcount = testcount + 1
    #test if we can write to csv file - **FORCED**
    s.write_csv(odir, "output_test{}.csv".format(testcount))
    #we will do test *not* using readers but by comparing lines
    efn = os.path.join(edir, "expect_test{}.csv".format(testcount))
    ofn = os.path.join(odir, "output_test{}.csv".format(testcount))
    elines, olines = [], []
    with open(efn, 'r') as f:
        elines = f.readlines()
    with open(ofn, 'r') as f:
        olines = f.readlines()
    statuses.append(all([(e == o) for (e, o) in zip(elines, olines)]))
    if not all(statuses):
        print("Failed TEST {}".format(testcount))

    #TEST 3
    testcount = testcount + 1
    #test if we can write to csv file - **DEFAULT**
    s.write_csv(odir)
    #we will do test *not* using readers but by comparing lines
    efn = os.path.join(edir, "expect_test{}.csv".format(testcount))
    ofn = os.path.join(odir, "test.csv".format(testcount))
    elines, olines = [], []
    with open(efn, 'r') as f:
        elines = f.readlines()
    with open(ofn, 'r') as f:
        olines = f.readlines()
    statuses.append(all([(e == o) for (e, o) in zip(elines, olines)]))
    if not all(statuses):
        print("Failed TEST {}".format(testcount))
    
    #TEST 4
    testcount = testcount + 1
    #test if we can subset when wavelengths are integers
    dm = np.array([[340, 0.1234], [341, 0.2234], [342, 0.3234], 
                   [343, 0.4234], [344, 0.5234], [345, 0.6234]], 
                   dtype = np.double)
    idstr = "test"
    company = "csv"
    instrument = "csv"
    s = Spectrum(dm, idstr, company, instrument)
    sub = s.wavelength_subset(341.0, 344.0)
    subexpwaves = np.array([341, 342, 343, 344], 
                           dtype = np.double)
    subexprefls = np.array([0.2234, 0.3234, 0.4234, 0.5234], 
                           dtype = np.double)
    statuses.append(np.array_equal(sub.wavelengths, subexpwaves))
    statuses.append(np.array_equal(sub.reflectances, subexprefls))
    if not all(statuses):
        print("Failed TEST {}".format(testcount))


    #TEST 5
    testcount = testcount + 1
    #test if we can subset when wavelengths are integers
    dm = np.array([[340.4, 0.1234], [341.1, 0.2234], [342.3, 0.3234], 
                   [343.2, 0.4234], [344.4, 0.5234], [345.6, 0.6234]], 
                   dtype = np.double)
    idstr = "test"
    company = "csv"
    instrument = "csv"
    s = Spectrum(dm, idstr, company, instrument)
    sub = s.wavelength_subset(341.0, 344.0)
    subexpwaves = np.array([341.1, 342.3, 343.2, 344.4], 
                        dtype = np.double)
    subexprefls = np.array([0.2234, 0.3234, 0.4234, 0.5234], 
                        dtype = np.double)
    statuses.append(np.array_equal(sub.wavelengths, subexpwaves))
    statuses.append(np.array_equal(sub.reflectances, subexprefls))
    if not all(statuses):
        print("Failed TEST {}".format(testcount))        

    #status message
    if all(statuses):
        print("{}: PASSED".format(__file__))
    else:
        print("{}: FAILED".format(__file__))
    
    
    
if __name__ == "__main__":
    testsdir = "/home/prabu/mycode/sdal/tests_data/test_Spectrum"
    verbose = False
    test(testsdir,
         verbose)