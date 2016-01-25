# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 18:12:12 2015

@author: pravindran
"""

from __future__ import print_function
import numpy as np
from ReaderHelper import ReaderHelper
from helpers import get_directory_filename_extension


class CsvReader:
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
                                                           headersep = "=",
                                                           datasep = ",")
        #get the numerical data
        dm = rh.read_spectrum_data(filename,
                                   numskiprows = nskip,
                                   wavecol = wcol,
                                   reflcol = rcol,
                                   datasep = ",")
        #if tags are mentioned in file use those inplace of init/default
        if "sdal_idstr" in hdr: idstr = hdr["sdal_idstr"]
        if "sdal_company" in hdr: company = hdr["sdal_company"]        
        if "sdal_instrument" in hdr: instrument = hdr["sdal_instrument"]  
        #return details
        return (dm, idstr, company, instrument)

             
if __name__ == "__main__":
    print("CsvReaderWriter.py")
    