# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 18:03:49 2015

@author: pravindran
"""

from __future__ import print_function
import struct
import numpy as np
import sys
from helpers import get_directory_filename_extension

class AsdReader:
    def __init__(self):
        self._instrtype = ["UNKNOWN", 
                           "PSII", 
                           "LSVNIR", 
                           "FSVNIR",
                           "FSFR",
                           "FSNIR",
                           "CHEM",
                           "FSFRUNATT"]

    
    def read_spectrum(self, filename):
        #read the contents of the binary file
        binconts = None
        with open(filename, 'rb') as f:
            binconts = f.read()
        #the file version
        fileversion = "".join(struct.unpack("ccc", binconts[0:(0 + 3)]))
        #the instrument number
        instnumber = str(struct.unpack("H", binconts[400:(400 + 2)])[0])
        #the instrument model
        instmodel = struct.unpack("B", binconts[431:(431 + 1)])[0]
        instmodel = self._instrtype[int(instmodel)]
        #start wavelength
        wavestart = struct.unpack("f", binconts[191:(191 + 4)])[0]
        #step wavelength
        wavestep = struct.unpack("f", binconts[195:(195 + 4)])[0]
        #data format
        data_format = struct.unpack("B", binconts[199:(199 + 1)])[0]
        #number of channels
        numchannels = struct.unpack("h", binconts[204:(204 + 2)])[0]
        #construct wavelength vector
        wavestop = wavestart + numchannels*wavestep - 1
        wavs = np.linspace(wavestart, wavestop, numchannels)
        #format string to unpack target and reference values
        fmt = "f"*numchannels                                 
        if data_format == 2:
            fmt = 'd'*numchannels
        if data_format == 0:
            fmt = 'f'*numchannels
        size = numchannels*8

        refls = []
        if fileversion == 'ASD':
            refls = np.array(struct.unpack(fmt, binconts[484:(484 + size)]))
        if fileversion == 'as7':
            tgts = np.array(struct.unpack(fmt, binconts[484:(484 + size)]))
            ref_flag = struct.unpack('?', binconts[484 + size: 484 + size + 1])[0]
            print("filename = {}, ref_flag = {}".format(filename, ref_flag))
            desc_length = struct.unpack('H', binconts[484 + size + 18: 484 + size + 18 + 2])[0]
            print("desc_length = {}".format(desc_length))
            print("size = {}".format(size))
            #'H' with 2 bytes works
            
            #HACK: search for best set of values
            buff = 50 #used to be 50
            minptp = 1000000.0
            refstart = -1
            for s in range(17712 - buff, 17712 + buff):
                if (s + size) < len(binconts):
                    tmp = np.array(struct.unpack(fmt, binconts[s:(s + size)]))
                    if np.min(tmp) > 1.0 and np.max(tmp) > 50.0 and np.ptp(tmp) < minptp:
                            minptp = np.ptp(tmp)
                            refstart = s
            refs = np.array([])
            if refstart > -1:
                refs = np.array(struct.unpack(fmt, binconts[refstart:(refstart + size)])) 
            #compute reflectances
            refls = tgts
            #refls = tgts/refs #original
            print(tgts)
            print(refs)
          
        
#        #read target values
##        tgts = np.array(struct.unpack(fmt, binconts[484:(484 + size)]))
#        tgts = np.array(struct.unpack(fmt, binconts[484:(484 + size)]))
#        print(tgts[:50])
#        return 
#        
#        
#        #read reference values
##        refs = np.array(struct.unpack(fmt, binconts[17712:(17712 + size)]))
#        #HACK: search for best set of values
#        buff = 50
#        minptp = 1000000.0
#        refstart = -1
#        for s in range(17712 - buff, 17712 + buff):
#            if (s + size) < len(binconts):
#                tmp = np.array(struct.unpack(fmt, binconts[s:(s + size)]))
#                if np.min(tmp) > 0.0 and np.max(tmp) > 50.0 and np.ptp(tmp) < minptp:
#                    minptp = np.ptp(tmp)
#                    refstart = s
#        refs = np.array([])
#        if refstart > -1:
#            refs = np.array(struct.unpack(fmt, binconts[refstart:(refstart + size)])) 
#                             
#        #compute reflectances
#        refls = tgts/refs
#      
        #create and return Spectrum object
        if np.size(refls) == numchannels:
            (d, f, e) = get_directory_filename_extension(filename)
            idstr = f
            company = "asd"
            instrument = "_".join([instmodel, instnumber, fileversion])
            return (np.column_stack((wavs, refls)), idstr, company, instrument)
        else:
            print("AsdReader: reflectances not read")
            sys.exit(0)
        
        
if __name__ == "__main__":
    print("AsdReader.py")
    