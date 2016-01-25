# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 11:57:37 2015

@author: pravindran
"""

from __future__ import print_function
import sys
import os, os.path
import shutil
import argparse
from helpers import get_directory_filename_extension

if __name__ == "__main__":
    print("+++++++++++++++++++++\n\n")
    print('filename_space_remover.py')
    
    #setup a parser
    par = argparse.ArgumentParser()
    par.add_argument("--input_directory",
                     type = str,
                     required = True,
                     dest = "input_directory")
    par.add_argument("--substitute_character",
                     type = str,
                     required = False,
                     default = '_',
                     dest = "substitute_character")
    par.add_argument("--recursive",
                     action = 'store_true',
                     default = False,
                     dest = "recursive")        
    
    #parse it
    params = par.parse_known_args(sys.argv[1:])[0].__dict__
    in_dir = params['input_directory']
    sub_char = params['substitute_character']
    recursive = params['recursive']
    
    #get the list of filenames
    filenames = []
    if recursive:
        for root, dirs, files in os.walk(in_dir):
            for f in files:
                filenames.append(os.path.join(root, f))
    else:
        filenames = [os.path.join(in_dir, f) for f in os.listdir(f)
                                             is os.path.isfile(f)]
                                            
    
    #make the changes
    for srcf in filenames:
        d, f, e = get_directory_filename_extension(srcf)
        tkns = f.split()
        if len(tkns) > 1:
            dstf = os.path.join(d, sub_char.join(tkns) + "." + e)
            shutil.copyfile(srcf, dstf)