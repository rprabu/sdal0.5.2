# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 15:00:27 2015

@author: pravindran
"""

from __future__ import print_function
import numpy as np
from ReaderHelper import ReaderHelper
from helpers import get_directory_filename_extension


class SigReader:
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
                                                           headersep = "=")
        #get the numerical data
        dm = rh.read_spectrum_data(filename,
                                   numskiprows = nskip,
                                   wavecol = wcol,
                                   reflcol = rcol)
        #if tags are mentioned in file use those inplace of init/default
        if "name" in hdr: 
            idstr = get_directory_filename_extension(hdr["name"])[1]
#            print("SigReader: idstr = {}".format(idstr))
        company = "sig"        
        if "instrument" in hdr: 
            instrument = hdr["instrument"].strip()  
        #return details
        return (dm, idstr, company, instrument)
    
    
if __name__ == "__main__":
    print("SigReader.py")
    
        