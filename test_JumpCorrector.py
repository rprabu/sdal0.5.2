# -*- coding: utf-8 -*-
"""
Created on Fri May 22 16:21:34 2015

@author: prabu
"""

from __future__ import print_function
import os, os.path
import numpy as np
import matplotlib.pyplot as plt
from SdalReader import SdalReader
from JumpCorrector import JumpCorrector

def test(testsdir, verbose = False):
    statuses = []

    
    #load the spectrums    
    indir = os.path.join(testsdir, "input")
    infs = [os.path.join(indir, "test_asdspec1_njc.txt"),
            os.path.join(indir, "test_asdspec2_njc.txt")]
    exdir = os.path.join(testsdir, "expect")
    exfs = [os.path.join(exdir, "test_asdspec1_jc.txt"),
            os.path.join(exdir, "test_asdspec2_jc.txt")]
    ins = [SdalReader().read_spectrum(f) for f in infs]
    exs = [SdalReader().read_spectrum(f) for f in exfs]

        
    #test 1    
    jumpwaves = [1000, 1800]    
    stablezone = 0
    jcorr = JumpCorrector(jumpwavelengths = jumpwaves, 
                          stablezone = stablezone)
    jcs = [jcorr.correct(s) for s in ins]
    for (e, j) in zip(exs, jcs):
        statuses.append(np.allclose(e.data, j.data, atol = 0.0001))
    
        
    #status message
    if all(statuses):
        print("{}: PASSED".format(__file__))
    else:
        print("{}: FAILED".format(__file__))
        

    #plot for ecosis sdal talk
    jumpwaves = [1000, 1800]
    stablezone = 0
    jcorr = JumpCorrector(jumpwavelengths = jumpwaves, 
                          stablezone = stablezone)
    jcs = [jcorr.correct(s) for s in ins]
    fig1, axes1 = plt.subplots(nrows = 1, ncols = 2)
    axes1[0].plot(ins[0].wavelengths, ins[0].reflectances, 'r')
    axes1[1].plot(ins[0].wavelengths, ins[0].reflectances, 'r')
    axes1[1].plot(jcs[0].wavelengths, jcs[0].reflectances, 'g')
    title = "L: Input, R: Corrected, Jump wavelengths = 1000, 1800"
    fig1.suptitle(title)
    fig1.show()
    fig1.savefig("ecosis-talk-jump-correction.png")

    
    #test 2 jumpwaves, stablezone = 0
#    jumpwaves = [1000, 1800]
#    stablezone = 0
#    jcorr = JumpCorrector(jumpwavelengths = jumpwaves, 
#                          stablezone = stablezone)
#    jcs = [jcorr.correct(s) for s in ins]
#    fig1, axes1 = plt.subplots(nrows = 1, ncols = 2)
#    for i in range(len(exs)):
#        axes1[i].plot(ins[i].wavelengths, ins[i].reflectances, 'r')
#        axes1[i].plot(jcs[i].wavelengths, jcs[i].reflectances, 'g')
#    title = "Jumpwavelengths = {}, stablezone = {}"
#    fig1.suptitle(title.format(jumpwaves, stablezone))
#    fig1.show()
    
#    #test 2 jumpwaves, stablezone = 1
#    jumpwaves = [1000, 1800]
#    stablezone = 1
#    jcorr = JumpCorrector(jumpwavelengths = jumpwaves, 
#                          stablezone = stablezone)
#    jcs = [jcorr.correct(s) for s in ins]
#    fig1, axes1 = plt.subplots(nrows = 1, ncols = 2)
#    for i in range(len(exs)):
#        axes1[i].plot(ins[i].wavelengths, ins[i].reflectances, 'r')
#        axes1[i].plot(jcs[i].wavelengths, jcs[i].reflectances, 'g')
#    title = "Jumpwavelengths = {}, stablezone = {}"
#    fig1.suptitle(title.format(jumpwaves, stablezone))
#    fig1.show()
#    
#    #test 2 jumpwaves, stablezone = 2
#    jumpwaves = [1000, 1800]
#    stablezone = 2
#    jcorr = JumpCorrector(jumpwavelengths = jumpwaves, 
#                          stablezone = stablezone)
#    jcs = [jcorr.correct(s) for s in ins]
#    fig1, axes1 = plt.subplots(nrows = 1, ncols = 2)
#    for i in range(len(exs)):
#        axes1[i].plot(ins[i].wavelengths, ins[i].reflectances, 'r')
#        axes1[i].plot(jcs[i].wavelengths, jcs[i].reflectances, 'g')
#    title = "Jumpwavelengths = {}, stablezone = {}"
#    fig1.suptitle(title.format(jumpwaves, stablezone))
#    fig1.show()
#
#    #test 1 jumpwave, stablezone = 0
#    jumpwaves = [1000]
#    stablezone = 0
#    jcorr = JumpCorrector(jumpwavelengths = jumpwaves, 
#                          stablezone = stablezone)
#    jcs = [jcorr.correct(s) for s in ins]
#    fig1, axes1 = plt.subplots(nrows = 1, ncols = 2)
#    for i in range(len(exs)):
#        axes1[i].plot(ins[i].wavelengths, ins[i].reflectances, 'r')
#        axes1[i].plot(jcs[i].wavelengths, jcs[i].reflectances, 'g')
#    title = "Jumpwavelengths = {}, stablezone = {}"
#    fig1.suptitle(title.format(jumpwaves, stablezone))
#    fig1.show()
#
#    #test 1 jumpwave, stablezone = 1
#    jumpwaves = [1800]
#    stablezone = 1
#    jcorr = JumpCorrector(jumpwavelengths = jumpwaves, 
#                          stablezone = stablezone)
#    jcs = [jcorr.correct(s) for s in ins]
#    fig1, axes1 = plt.subplots(nrows = 1, ncols = 2)
#    for i in range(len(exs)):
#        axes1[i].plot(ins[i].wavelengths, ins[i].reflectances, 'r')
#        axes1[i].plot(jcs[i].wavelengths, jcs[i].reflectances, 'g')
#    title = "Jumpwavelengths = {}, stablezone = {}"
#    fig1.suptitle(title.format(jumpwaves, stablezone))
#    fig1.show()

    
if __name__ == "__main__":
    print("Testing JumpCorrector class")
    testsdir = "/home/prabu/mycode/sdal/tests_data/test_JumpCorrector/"
    test(testsdir, False)