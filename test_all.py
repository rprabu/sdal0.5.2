# -*- coding: utf-8 -*-
"""
Created on Mon May  4 02:45:57 2015

@author: prabu
"""

from __future__ import print_function
import sys
import os, os.path
import test_Spectrum
import test_SpectrumGroup
import test_SdalReader
import test_WaveUniquifier
import test_WaveResampler
import test_ReferenceDetector


if __name__ == "__main__":
    testsdir = sys.argv[1]
    test_Spectrum.test(os.path.join(testsdir, "test_Spectrum"))
    test_SpectrumGroup.test(os.path.join(testsdir, "test_SpectrumGroup"))
    test_SdalReader.test(os.path.join(testsdir, "test_SdalReader"))
    test_WaveUniquifier.test(os.path.join(testsdir, "test_WaveUniquifier"))
    test_WaveResampler.test(os.path.join(testsdir, "test_WaveResampler"))
    test_ReferenceDetector.test(os.path.join(testsdir, "test_ReferenceDetector"))