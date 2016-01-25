# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 08:12:53 2015

@author: pravindran
"""

from __future__ import print_function
import os, os.path
import sys
import argparse
from SdalReader import SdalReader
from OverlapHandler import OverlapHandler
from GreenVegDetector import GreenVegDetector
from SpectrumRegex import SpectrumRegex
from SpectrumGroup import SpectrumGroup
from helpers import get_extension
from sdal_save_data import save_data


def process_directory(params):
    
    #parameters for processing
    input_dir = params["input_directory"]
    ws = params["subset_wavelength_range"][0]
    we = params["subset_wavelength_range"][1]
    pattern = params["grouping_pattern"]
    patt_name = params['grouping_output_name']
    
    #read the spectrums    
    extension = 'sig'
    spec_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) 
                                             if get_extension(f) == extension]
#    for f in spec_files:
#        print(f)
    raw_specs = [SdalReader().read_spectrum(f) for f in spec_files]
    if len(raw_specs) == 0: 
        return    
#    print("Data directory: {}".format(input_dir))
#    print("  Read {} {} files".format(len(raw_specs), extension))
#    for s in raw_specs:
#        print(s.idstr)
    
        
    #uniquify wavelengths and interpolate to 1nm
    ohr = OverlapHandler(rstype = 'linear')
    rs_specs = []
    for s in raw_specs:
        if ohr.is_1nm(s):
            rs_specs.append(s)
        else:
            rs_specs.append(ohr.process_overlap(s))
    print("  Uniquified and monotoned spectrums")
    
#    for w in rs_specs[0].wavelengths:
#        print(w)
    
    #separate into green vegetation and non-green vegetation spectra
    gvd = GreenVegDetector()
    raw_white_specs, raw_target_specs = [], []
    rs_white_specs, rs_target_specs = [], []
    ndvis, reflectance_ranges = [], []
    for (raw, rs) in zip(raw_specs, rs_specs):
        (status, ndvi, reflectance_range) = gvd.is_green_vegetation(rs)
        ndvis.append(ndvi)
        reflectance_ranges.append(reflectance_range)
        if status:
            raw_target_specs.append(raw)
            rs_target_specs.append(rs)
        else:
            raw_white_specs.append(raw)
            rs_white_specs.append(rs)
    print("   # white spectra: {}".format(len(rs_white_specs)))
    print("   # target spectra: {}".format(len(rs_target_specs)))

    
    #subset to desired wavelength range
    #do this for the jc_target_specs only
    proc_target_specs = [s.wavelength_subset(ws, we) for s in rs_target_specs]
    print("   Subsetted spectra to range: {}, {}".format(ws, we))

        
    #identify groups using SpectrumRegex and create SpectrumGroup objects
    grps_dict = SpectrumRegex().make_groups(proc_target_specs, pattern)
#    for k in grps_dict:
#        print(k, len(grps_dict[k]))
#        SpectrumGroup().group(grps_dict[k], k)
    patt_groups = [SpectrumGroup().group(grps_dict[k], k) for k in grps_dict]
    print("   Grouped spectrums: {} groups".format(len(patt_groups)))    
    
    #create output directories and save data    
    save_data(input_dir, 
              raw_white_specs, 
              raw_target_specs, 
              proc_target_specs,
              patt_name,
              patt_groups)
              
              
if __name__ == "__main__":

    print("\n\n\n")
    #setup a parser
    par = argparse.ArgumentParser()
    par.add_argument("--input_directory",
                     type = str,
                     required = True,
                     dest = "input_directory")
    par.add_argument("--subset_wavelength_range",
                     type = float,
                     nargs = 2,
                     required = False,
                     default = [350, 2500],
                     dest = "subset_wavelength_range")
    par.add_argument("--grouping_output_name",
                     type = str,
                     required = True,
                     dest = "grouping_output_name")
    par.add_argument("--grouping_pattern",
                     type = str,
                     required = True,
                     dest = "grouping_pattern",
                     help = "e.g. *-X OR *_X for leaf level averaging")
    par.add_argument("--recursive",
                     action = 'store_true',
                     default = False,
                     dest = "recursive") 
                     
    #parse it
    params = par.parse_known_args(sys.argv[1:])[0].__dict__
    
    #the directories that need to be processed
    indirs = []
    indirs.append(params["input_directory"])
    if params["recursive"]:
        for root, dirs, files in os.walk(params["input_directory"]):
            for d in dirs:
                indirs.append(os.path.join(root, d))
    
    #do the processing
    for d in indirs:
        params['input_directory'] = d
        process_directory(params)
    
    print("\n\n\n")