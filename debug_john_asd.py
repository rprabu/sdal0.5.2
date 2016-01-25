# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from __future__ import print_function
import os, os.path
import sys
import argparse
from SdalReader import SdalReader
from JumpCorrector import JumpCorrector
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
    extension = {'asd': 1, 'ASD': 1}
    spec_files = [os.path.join(input_dir, f) for f in sorted(os.listdir(input_dir)) 
                                             if get_extension(f) in extension]
    raw_specs = [SdalReader().read_spectrum(f) for f in spec_files]
    if len(raw_specs) == 0: return    
    
#    #perform jump correction
#    jumpcorrector = JumpCorrector(params["jumpcorrection_wavelengths"],
#                                  params["jumpcorrection_stablezone"])
#    jc_specs = [jumpcorrector.correct(s) for s in raw_specs]
#    print("   Jump corrected {} spectrums(s)".format(len(jc_specs)))
#    
#    
#    #separate into green vegetation and non-green vegetation spectra
#    gvd = GreenVegDetector()
#    raw_white_specs, raw_target_specs = [], []
#    jc_white_specs, jc_target_specs = [], []
#    ndvis, reflectance_ranges = [], []
#    for (raw, jc) in zip(raw_specs, jc_specs):
#        (status, ndvi, reflectance_range) = gvd.is_green_vegetation(jc)
#        ndvis.append(ndvi)
#        reflectance_ranges.append(reflectance_range)
#        if status:
#            raw_target_specs.append(raw)
#            jc_target_specs.append(jc)
#        else:
#            raw_white_specs.append(raw)
#            jc_white_specs.append(jc)
#    print("   # white spectra: {}".format(len(jc_white_specs)))
#    print("   # target spectra: {}".format(len(jc_target_specs)))
#
#    
#    #subset to desired wavelength range
#    #do this for the jc_target_specs only
#    proc_target_specs = [s.wavelength_subset(ws, we) for s in jc_target_specs]
#    print("   Subsetted spectra to range: {}, {}".format(ws, we))
#
#        
#    #identify groups using SpectrumRegex and create SpectrumGroup objects
#    patt_groups = []
#    grps_dict = SpectrumRegex().make_groups(proc_target_specs, pattern)
#    patt_groups = [SpectrumGroup().group(grps_dict[k], k) for k in grps_dict]
#    print("   Grouped spectrums: {} groups".format(len(patt_groups)))    
#    
#    #create output directories and save data    
#    save_data(input_dir, 
#              raw_white_specs, 
#              raw_target_specs, 
#              proc_target_specs,
#              patt_name,
#              patt_groups)


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
    par.add_argument("--jumpcorrection_wavelengths",
                     type = float,
                     nargs = 2,
                     required = False,
                     default = [1000, 1800],
                     dest = "jumpcorrection_wavelengths")
    par.add_argument("--jumpcorrection_stablezone",
                     type = int,
                     required = False,
                     default = 0,
                     dest = "jumpcorrection_stablezone")
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