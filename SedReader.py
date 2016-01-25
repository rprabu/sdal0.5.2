# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 16:38:14 2015

@author: pravindran
"""

from __future__ import print_function
import numpy as np
from ReaderHelper import ReaderHelper
from helpers import get_directory_filename_extension


class SedReader:
    def __init__(self):
        pass


    def read_spectrum(self,
                      filename):
        #split the filename to get init/default values
        (d, f, e) = get_directory_filename_extension(filename)
        idstr = f
        company = e
        instrument = company
        #initialize data to empty matrix
        dm = np.array([])
        #get header data
        rh = ReaderHelper()
        (nskip, wcol, rcol, hdr) = rh.read_spectrum_header(filename, 
                                                           headersep = ":")
        #get the numerical data
        dm = rh.read_spectrum_data(filename,
                                   numskiprows = nskip,
                                   wavecol = wcol,
                                   reflcol = rcol)
        #if tags are mentioned in file use those inplace of init/default
        if "File Name" in hdr: 
            idstr = get_directory_filename_extension(hdr["File Name"])[1]
        company = "sed"        
        if "Instrument" in hdr: instrument = hdr["Instrument"].strip()  
        #return details
        return (dm, idstr, company, instrument)
            
    
if __name__ == "__main__":
    print("SedReader.py")
    
    
    
    