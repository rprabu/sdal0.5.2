# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 15:22:04 2015

@author: pravindran
"""

from __future__ import print_function
import numpy as np
import os, os.path
import sys
from helpers import closest_array_index


class Spectrum:
    
    def __init__(self, 
                 data = np.array([]), 
                 idstr = "", 
                 company = "",
                 instrument = "",
                 metadata = {}):
        self._idstr = ""
        self._company = ""
        self._instrument = ""
        self._jumpvalues = []
        self._jumpwavelengths = []
        self._is_reference = False
        self._metadata = {}
        self._create(data,
                     idstr,
                     company,
                     instrument,
                     metadata)
        
        
    def write_csv(self, odir, filename = ""):
        #construct the destination filename
        f = ""
        if filename:
            f = os.path.join(odir, filename)
        else:
            f = os.path.join(odir, ".".join([self.idstr, "csv"]))
        #construct the lines that will be dumped into file
        #the header lines        
        hdrlines = []
        hdrlines.append("=".join(["sdal_idstr", self.idstr]))
        hdrlines.append("=".join(["sdal_company", self.company]))
        hdrlines.append("=".join(["sdal_instrument", self.instrument]))
        hdrlines.append("=".join(["sdal_date", "1-1-2015"]))
        hdrlines.append("=".join(["sdal_latitude", "NA"]))
        hdrlines.append("=".join(["sdal_longitude", "NA"]))
        hdrlines.append("\n")
        hdrstr = "\n".join(hdrlines)
        #write it out using numpy
        np.savetxt(f, 
                   self.data, 
                   header = hdrstr, 
                   fmt = "%.1f, %0.15f", 
                   comments = "")

    
    def wavelength_subset(self, wavestart, wavestop):
        idx1 = closest_array_index(wavestart, self.wavelengths)
        idx2 = closest_array_index(wavestop, self.wavelengths) + 1
        return Spectrum(data = self._data[idx1:idx2, :],
                        idstr = self._idstr,
                        company = self._company,
                        instrument = self._instrument)
    
    
    def num_wavelengths(self):
        return np.shape(self._data)[0]

    
    def wavelength_range(self):
        return (self.data[0, 0], self.data[-1, 0])
        
        
    def header_string(self, delimiter = "\n"):
        return delimiter.join([self._idstr, self._company, self._instrument])
    
    def _create(self,
                data,
                idstr,
                company,
                instrument,
                metadata):
        if (isinstance(data, np.ndarray) and 
            (np.size(data) >= 2) and 
            (np.size(data) % 2 == 0)):
            self._data = np.copy(data)
        else:
            print("Spectrum: Invalid arg")
            sys.exit(0)
        self._idstr = idstr
        self._company = company
        self._instrument = instrument
        for k in metadata:
            self._metadata[k] = metadata[k]

    
    #data access    
    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, datamatrix):
        self._data = np.copy(datamatrix)
       
       
    @property
    def wavelengths(self):
        if self._data is not None:
            return self._data[:, 0]
        return None

   
    @property
    def reflectances(self):
        if self._data is not None:
            return self._data[:, 1]
        return None
        
        
    @property
    def idstr(self):
        return self._idstr
    @idstr.setter
    def idstr(self, idstr):
        self._idstr = idstr


    @property
    def company(self):
        return self._company
    @company.setter
    def company(self, company):
        self._company = company


    @property
    def instrument(self):
        return self._instrument
    @instrument.setter
    def instrument(self, instrument):
        self._instrument = instrument
        
        
    @property
    def is_reference(self):
        return self._is_reference
    @is_reference.setter
    def is_reference(self, status):
        self._is_reference = status


    #jump correction    
    @property
    def jumpvalues(self):
        return self._jumpvalues
    @jumpvalues.setter
    def jumpvalues(self, jmpvalues):
        self._jumpvalues = list(jmpvalues)

            
    @property
    def jumpwavelengths(self):
        return self._jumpwavelengths
    @jumpwavelengths.setter
    def jumpwavelengths(self, jmpwavelengths):
        self._jumpwavelengths = list(jmpwavelengths)

        
    def metadata(self, key = ""):
        if key and key in self._metadata:
            return self._metadata[key]
        return self._metadata
        
        
    def print_jump_data(self):
        print("jumpvalues = {}".format(self.jumpvalues))
        print("jumpwavelengths = {}".format(self.jumpwavelengths))
        
          

if __name__ == "__main__":
   print("Spectrum.py")
    
    