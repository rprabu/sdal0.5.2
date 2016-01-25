# -*- coding: utf-8 -*-
"""
Created on Sat May  2 13:00:57 2015

@author: pravindran
"""

from __future__ import print_function
import os, os.path
import sys
import numpy as np
from Spectrum import Spectrum
from CsvReader import CsvReader
from AsdReader import AsdReader
from SedReader import SedReader
from SigReader import SigReader
from EnviReader import EnviReader
from helpers import get_directory_filename_extension

class SdalReader:
    #-------------------------------------------------------------------------
    def __init__(self):
        pass
    
    #-------------------------------------------------------------------------    
    def read_spectrum(self, 
                      filename,
                      ancillary_filename = ""):
        #check validity of filename
        if not os.path.exists(filename) or not os.path.isfile(filename):
            print("{}: {} is invalid".format(__file__, filename))
            sys.exit(0)
        #choose reader based on file extension 
        ext = get_directory_filename_extension(filename)[2]
        dm, idstr, co, instr = np.array([]), "", "", ""
        if ext == "csv" or ext == "txt":
            (dm, idstr, co, instr) = CsvReader().read_spectrum(filename)
        elif ext == "asd" or ext == 'ASD':
            (dm, idstr, co, instr) = AsdReader().read_spectrum(filename)
        elif ext == "sed":
            (dm, idstr, co, instr) = SedReader().read_spectrum(filename)
        elif ext == "sig":
            (dm, idstr, co, instr) = SigReader().read_spectrum(filename)
#            print("Sdal Reader: idstr = {}".format(idstr))
        else:
            print("{}: Invalid file type {}".format(__file__, ext))
            sys.exit(0)
        return Spectrum(dm, idstr, co, instr)
        
    #-------------------------------------------------------------------------
    def read_spectrums(self, filename, ancillary1 = ""):
         #check validity of filename
        if not os.path.exists(filename) or not os.path.isfile(filename):
            print("{}: {} is invalid".format(__file__, filename))
            sys.exit(0)
        if not os.path.exists(ancillary1) or not os.path.isfile(ancillary1):
            print("{}: {} is invalid".format(__file__, ancillary1))
            sys.exit(0)
        #choose reader based on file extension 
        ext = get_directory_filename_extension(filename)[2]
        dms, idstrs, cos, instrs = [], [], [], []
        if ext == "sli":
            (dms, idstrs, cos, instrs) = EnviReader().read_spectrums(filename,
                                                                   ancillary1)
                                                    
        return [Spectrum(dms[i], idstrs[i], cos[i], instrs[i]) 
                for i in range(len(dms))]

                
if __name__ == "__main__":
    print("SdalReader.py")