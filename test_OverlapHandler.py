# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 14:12:49 2015

@author: prabu
"""

from __future__ import print_function
import os, os.path
import matplotlib.pyplot as plt
from SdalReader import SdalReader
from OverlapHandler import OverlapHandler

if __name__ == "__main__":
    print("Testing the OverlapHandler class")
    
    testdir = "/home/prabu/mycode/sdal/tests_data/test_OverlapHandler"
    
    
    signames = ["gr082014_000.sig", "gr082014_001.sig"]
    sigfiles = [os.path.join(testdir, "input", f) for f in signames]
    sigspec = [SdalReader().read_spectrum(f) for f in sigfiles]
    
    oh = OverlapHandler()
    ohdspec = [oh.process_overlap(s) for s in sigspec]
    
    #plot it to see if it looks correct
    fig1, axes1 = plt.subplots(nrows = 2, ncols = 1)
    for i in range(len(ohdspec)):
        axes1[i].set_xlim([300.0, 2600.0])
        axes1[i].set_ylim([0.0, 1.0])
        axes1[i].plot(ohdspec[i].wavelengths, 
                      ohdspec[i].reflectances + 0.1, 
                      color = 'g',
                      alpha = 0.6,
                      label = "After overlap handling")
        axes1[i].plot(sigspec[i].wavelengths, 
                      sigspec[i].reflectances, 
                      color = 'r',
                      alpha = 0.6,
                      label = "Before overlap handling")
        legend = axes1[i].legend(loc = 'upper center', shadow = True)
    fig1.suptitle("Spectra with and without overlap handling")
    fig1.show()
    