# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 15:24:19 2015

@author: prabu
"""

from __future__ import print_function
import os, os.path 
import re
import matplotlib.pyplot as plt
from SdalReader import SdalReader
from JumpCorrector import JumpCorrector
from OutlierDetector import OutlierDetector

if __name__ == "__main__":
    print("test_OutlierDetector.py")
    
    #get the files into benas, emnis and vauls
    tdir = "/home/prabu/mycode/sdal/tests_data/test_OutlierDetector"
    idir = os.path.join(tdir, "input")
    ifiles = os.listdir(idir)
    benafs = [os.path.join(idir, f) for f in ifiles if re.search(r'bena', f)]
    emnifs = [os.path.join(idir, f) for f in ifiles if re.search(r'emni', f)]
    vaulfs = [os.path.join(idir, f) for f in ifiles if re.search(r'vaul', f)]
    
    #read in the spectra
    benas = [SdalReader().read_spectrum(f) for f in benafs] 
    emnis = [SdalReader().read_spectrum(f) for f in emnifs]
    vauls = [SdalReader().read_spectrum(f) for f in vaulfs]
    specs = [benas, emnis, vauls]
    
    #jump correct
    jumpcorr = JumpCorrector(jumpwavelengths = [1000, 1800], stablezone = 0)
    benajcs = [jumpcorr.correct(s) for s in benas]
    emnijcs = [jumpcorr.correct(s) for s in emnis]
    vauljcs = [jumpcorr.correct(s) for s in vauls]
    specjcs = [benajcs, emnijcs, vauljcs]
    
    #compute outliers and inliers
    medians = []
    stds = []
    thresh = 3.0
    od = OutlierDetector(zthresh = thresh)
    for e in specjcs:
        (inliers, outliers) = od.detect(e)
        medians.append(od.median)
        stds.append(od.std)
        
    #plot the three types of spectra
    colors = ['red', 'green', 'blue']
    fig1, axes1 = plt.subplots(nrows = 3, ncols = 1)
    for (i, a) in enumerate(axes1):
        a.set_xlim([300.0, 2600.0])
        a.set_ylim([0.0, 1.0])
        #draw the bands
        top = medians[i] + thresh*stds[i]
        bottom = medians[i] - thresh*stds[i]
        a.fill_between(specjcs[i][0].wavelengths, 
                       top, 
                       bottom,
                       color = '0.7')
        #draw the individual spectra
        for s in specjcs[i]:
            a.plot(s.wavelengths, 
                   s.reflectances,
                   color = colors[i],
                   alpha = 0.9)
        a.plot(specjcs[i][0].wavelengths,
               medians[i],
               color = 'black')
    fig1.suptitle("bena, emni, vaul spectra")
    fig1.show()
    fig1.savefig("iceland.pdf")
        
    print("benafs: \n{}\n".format("\n".join(sorted(benafs))))
    print("emnifs: \n{}\n".format("\n".join(sorted(emnifs))))
    print("vaulfs: \n{}\n".format("\n".join(sorted(vaulfs))))