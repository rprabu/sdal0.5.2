# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 13:18:15 2015

@author: pravindran
"""

from __future__ import print_function
import os, os.path 
from SdalReader import SdalReader
from sdal_plot_spectrums import plot_spectrums
from helpers import get_extension

if __name__ == "__main__":
    print("asd_trek.py")
    
    data_dir = '/home/pravindran/mycode/sdal_data/tests_data/asd_mixed_test/'
    files = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
    print("\n".join(files))
    
    specs = [SdalReader().read_spectrum(f) for f in files 
                                           if get_extension(f).lower() == 'asd']
    fig = plot_spectrums(specs,
                         spectrums_color = 'cyan',
                         title = "Spectra from ASD Trek + FieldSpec")
    fig.savefig(os.path.join(data_dir, "plots.pdf"))
    