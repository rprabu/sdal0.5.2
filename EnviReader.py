# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 22:43:50 2015

@author: prabu
"""

from __future__ import print_function
import numpy as np
import struct
import re
import sys

class EnviReader:

    #-------------------------------------------------------------------------    
    def __init__(self):
        pass
    
    #-------------------------------------------------------------------------    
    def read_spectrums(self, binfile, hdrfile):
        #read the header file
        fields = self._read_hdrfile(hdrfile)
        #read the contents of binfile
        binconts = None
        with open(binfile, 'rb') as f:
            binconts = f.read()
        #convert the binary to numbers
        if fields["interleave"] == "bsq":
            numwaves = len(fields["waves"])
            numnames = len(fields["names"])
            offset = fields["offset"]
            fmt = ''
            size = 0
            if fields["dtype"] == "4":
                fmt = 'f'*(numnames*numwaves)
                size = 8*numnames*numwaves
            start, stop = offset, (offset + size)
            nums = np.array(struct.unpack(fmt, binconts[start:stop]))
            nums = nums.reshape((numnames, numwaves))
        else:
            print("interleave = {} not implemented".format(fields["interleave"]))
            sys.exit(0)
        return ([], [], [], [])
    
    #-------------------------------------------------------------------------
    def _read_hdrfile(self, hdrfile):
        #read stuff from file
        conts = ""
        with open(hdrfile, 'r') as fh:
            conts = fh.read()
        
        #get the interleave
        m = re.search(r"interleave = (\w{3})", conts, re.MULTILINE)
        interleave = ""
        if m:
            interleave = str(m.group(1))
            
        #get the datatype
        m = re.search(r"data type = (\d)", conts, re.MULTILINE)
        dtype = ""
        if m:
            dtype = str(m.group(1))
            
        #get the header offset
        m = re.search(r"header offset = ([0-9])", conts, re.MULTILINE)
        offset = ""
        if m:
            offset = int(m.group(1))
            print("offset = {}".format(offset))
            
        #get the wavelengths
        m = re.search(r"wavelength = \{([^}]+)\}", conts, re.MULTILINE)
        waves = ""
        if m:
            waves = str(m.group(1))
            waves = [float(w) for w in waves.split(",")]
            
        #get the spectra names
        m = re.search(r"spectra names = \{([^}]+)\}", conts, re.MULTILINE)
        names = ""
        if m:
            names = str(m.group(1))
            names = [n.strip() for n in names.split(",")]
            
        fields = {"interleave": interleave,
                  "dtype": dtype,
                  "offset": offset,
                  "names": names,
                  "waves": waves}
        return fields


#-----------------------------------------------------------------------------
if __name__ == "__main__":
    print("EnviReader.py")
    
    