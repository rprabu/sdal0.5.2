# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 15:38:52 2015

@author: pravindran
"""

from __future__ import print_function
import os, os.path
import ntpath
import numpy as np


#----------------------------------------------------------------------------
def get_directory_filename_extension(filename):    
    d, f, e = "", "", ""
    if "\\" in filename:
        #this is windows style
        d = ntpath.split(filename)[0]
        (f, e) = ntpath.splitext(ntpath.basename(filename))
    else:
        #linux style
        d = os.path.split(filename)[0]
        (f, e) = os.path.splitext(os.path.basename(filename))
    if e:
        #convert .ext to ext
        e = e[1:]    
    return (d.strip(), f.strip(), e.strip())


#----------------------------------------------------------------------------
def get_extension(filename):
    return get_directory_filename_extension(filename)[2]


#----------------------------------------------------------------------------
def get_directory(filename):
    return get_directory_filename_extension(filename)[0]
    
    
#----------------------------------------------------------------------------        
def closest_array_index(val, arr):
    return np.argmin(np.abs(arr - float(val)))


#----------------------------------------------------------------------------
def closest_array_indices(vals, arr):
    return [closest_array_index(v, arr) for v in vals]


#----------------------------------------------------------------------------    
def list_of_eval(s):
    return list(eval(s))


#----------------------------------------------------------------------------
def are_same_arrays(arrs):
    if len(arrs) == 1:
        return True
    return all([np.array_equal(arrs[0], a) for a in arrs])    
    
    
    
    

    

    