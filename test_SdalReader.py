# -*- coding: utf-8 -*-
"""
Created on Sat May  2 22:49:09 2015

@author: pravindran
"""

from __future__ import print_function
import numpy as np
import os, os.path
from SdalReader import SdalReader


def test(testsdir,
         verbose = False):
    idir = os.path.join(testsdir, "input")
    edir = os.path.join(testsdir, "expect")
    statuses = []
    
    #CsvReader tests
    atol = 0.000001
    itmplt = "input_test{}.csv"
    ifs = [os.path.join(idir, itmplt.format(i)) for i in range(1, 8)]
    ispec = [SdalReader().read_spectrum(f) for f in ifs]
    etmplt = "expect_test{}.csv"    
    efs = [os.path.join(edir, etmplt.format(i)) for i in range(1, 8)]
    espec = [SdalReader().read_spectrum(f) for f in efs]
    for (idx, (i, e)) in enumerate(zip(ispec, espec)):
        statuses.append(i.idstr == e.idstr)
        statuses.append(i.company == e.company)
        statuses.append(i.instrument == e.instrument)
        statuses.append(np.allclose(i.wavelengths, e.wavelengths, atol = atol))
        statuses.append(np.allclose(i.reflectances, e.reflectances, atol = atol))
        if not all(statuses):
            print("Failed csv TEST {}".format(idx + 1))
    
    #AsdReader tests
    atol = 0.000001
    itmplt = "input_asd_test{}.asd"
    ifs = [os.path.join(idir, itmplt.format(i)) for i in range(1, 4)]
    ispec = [SdalReader().read_spectrum(f) for f in ifs]
    etmplt = "expect_asd_test{}.csv"    
    efs = [os.path.join(edir, etmplt.format(i)) for i in range(1, 4)]
    espec = [SdalReader().read_spectrum(f) for f in efs]
    for (idx, (i, e)) in enumerate(zip(ispec, espec)):
        statuses.append(i.idstr == e.idstr)
        statuses.append(i.company == e.company)
        statuses.append(i.instrument == e.instrument)
        statuses.append(np.allclose(i.wavelengths, e.wavelengths, atol = atol))
        statuses.append(np.allclose(i.reflectances, e.reflectances, atol = atol))
        if not all(statuses):
            print("Failed asd TEST {}".format(idx + 1))
            
    #SedReader tests
    atol = 0.0000001
    itmplt = "input_sed_test{}.sed"
    ifs = [os.path.join(idir, itmplt.format(i)) for i in range(1, 4)]
    ispec = [SdalReader().read_spectrum(f) for f in ifs]
    etmplt = "expect_sed_test{}.csv"    
    efs = [os.path.join(edir, etmplt.format(i)) for i in range(1, 4)]
    espec = [SdalReader().read_spectrum(f) for f in efs]
    for (idx, (i, e)) in enumerate(zip(ispec, espec)):
        statuses.append(i.idstr == e.idstr)
        statuses.append(i.company == e.company)
        statuses.append(i.instrument == e.instrument)
        statuses.append(np.allclose(i.wavelengths, e.wavelengths, atol = atol))
        statuses.append(np.allclose(i.reflectances, e.reflectances, atol = atol))
        if not all(statuses):
            print("Failed sed TEST {}".format(idx + 1))      
    
    #SigReader tests
    atol = 0.0000001
    itmplt = "input_sig_test{}.sig"
    ifs = [os.path.join(idir, itmplt.format(i)) for i in range(1, 4)]
    ispec = [SdalReader().read_spectrum(f) for f in ifs]
    etmplt = "expect_sig_test{}.csv"    
    efs = [os.path.join(edir, etmplt.format(i)) for i in range(1, 4)]
    espec = [SdalReader().read_spectrum(f) for f in efs]
    for (idx, (i, e)) in enumerate(zip(ispec, espec)):
        statuses.append(i.idstr == e.idstr)
        statuses.append(i.company == e.company)
        statuses.append(i.instrument == e.instrument)
        statuses.append(np.allclose(i.wavelengths, e.wavelengths, atol = atol))
        statuses.append(np.allclose(i.reflectances, e.reflectances, atol = atol))
        if not all(statuses):
            print("Failed sig TEST {}".format(idx + 1))      
    
    #status message
    if all(statuses):
        print("{}: PASSED".format(__file__))
    else:
        print("{}: FAILED".format(__file__))

        
            
if __name__ == "__main__":
    testsdir = "/home/prabu/mycode/sdal/tests_data/test_SdalReader"
    verbose = False
    test(testsdir,
         verbose)