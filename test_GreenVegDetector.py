# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 11:08:08 2015

@author: pravindran
"""

from __future__ import print_function
import os, os.path
from SdalReader import SdalReader
from GreenVegDetector import GreenVegDetector
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from helpers import get_extension



def test(adir, ext):
    #get the files in the data directory
    ext_files = [os.path.join(adir, f) for f in os.listdir(adir) 
                                        if get_extension(f) == ext]

    #read in the spectra 
    spectrums = [SdalReader().read_spectrum(f) for f in ext_files]
    print("# of {} spectrums: {}".format(ext, len(spectrums)))

    #separate the data into green vegetation and non-green vegetation
    green_veg_spectrums = []
    nongreen_veg_spectrums = []
    ndvis = []
    reflectance_ranges = []
    gvd = GreenVegDetector()
    for s in spectrums:
        status, ndvi, reflectance_range = gvd.is_green_vegetation(s) 
        ndvis.append(ndvi)
        reflectance_ranges.append(reflectance_range)
        if status:
            green_veg_spectrums.append(s)
        else:
            nongreen_veg_spectrums.append(s)    
    print("# green vegetation spectra: {}".format(len(green_veg_spectrums)))
    print("# non green vegetation spectra: {}".format(len(nongreen_veg_spectrums)))

    #plotting the green vegetation spectrums
    fig1 = plt.figure(figsize = (18, 5))
    ax1 = fig1.add_axes([0.1, 0.1, 0.7, 0.7])

    for s in green_veg_spectrums:
        ax1.plot(s.wavelengths, s.reflectances, color = 'green')
    ax1.axvline(x = gvd.ndvi_nir_range[0], ymin = 0.0, ymax = 1.0, 
                color = 'cyan')
    ax1.axvline(x = gvd.ndvi_nir_range[1], ymin = 0.0, ymax = 1.0, 
                color = 'cyan')
    ax1.axvline(x = gvd.ndvi_red_range[0], ymin = 0.0, ymax = 1.0, 
                color = 'yellow')
    ax1.axvline(x = gvd.ndvi_red_range[1], ymin = 0.0, ymax = 1.0, 
                color = 'yellow')

    ax1.set_xlim(left = 250, right = 2600)
    ax1.set_ylim(bottom = -0.1, top = 1.1)
    ax1.set_xlabel("Wavelengths", fontsize = 12)
    ax1.set_ylabel("Refletances", fontsize = 12)
    ax1.set_title("{} Green vegetation spectra".format(ext), fontsize = 15)
#    fig1.draw()

    #plotting the non-green vegetation spectrums
    fig2 = plt.figure(figsize = (18, 5))
    ax2 = fig2.add_axes([0.1, 0.1, 0.7, 0.7])

    for s in nongreen_veg_spectrums:
        ax2.plot(s.wavelengths, s.reflectances, color = 'red')
    ax2.axvline(x = gvd.ndvi_nir_range[0], ymin = 0.0, ymax = 1.0, 
                color = 'cyan')
    ax2.axvline(x = gvd.ndvi_nir_range[1], ymin = 0.0, ymax = 1.0, 
                color = 'cyan')
    ax2.axvline(x = gvd.ndvi_red_range[0], ymin = 0.0, ymax = 1.0, 
                color = 'yellow')
    ax2.axvline(x = gvd.ndvi_red_range[1], ymin = 0.0, ymax = 1.0, 
                color = 'yellow')

    ax2.set_xlim(left = 250, right = 2600)
    ax2.set_ylim(bottom = -0.1, top = 1.1)
    ax2.set_xlabel("Wavelengths", fontsize = 12)
    ax2.set_ylabel("Refletances", fontsize = 12)
    ax2.set_title("{} Non vegetation spectra".format(ext), fontsize = 15)
#    fig2.draw()

    #plotting ndvi and reflectance range
    fig3, axs3 = plt.subplots(1, 2, figsize = (16, 5))

    #plotting the ndvi values
    axs3[0].scatter(range(len(ndvis)), ndvis, color = 'black', alpha = 0.8)
    axs3[0].axhline(y = gvd.ndvi_thresh, xmin = 0.0, xmax = 1.0, color = 'red')
    axs3[0].set_xlim(left = 0, right = len(ndvis))
    axs3[0].set_ylim(bottom = -1.0, top = 1.0)
    axs3[0].set_xlabel("Spectrum index", fontsize = 12)
    axs3[0].set_ylabel("NDVI", fontsize = 12)
    axs3[0].set_title("{} spectra NDVIs".format(ext), fontsize = 15)


    #plotting the reflectance range values
    axs3[1].scatter(range(len(reflectance_ranges)), 
                    reflectance_ranges, 
                    color = 'black', alpha = 0.8)
    axs3[1].axhline(y = gvd.reflectance_range_thresh, 
                    xmin = 0.0, xmax = 1.0, color = 'red')
    axs3[1].set_xlim(left = 0, right = len(reflectance_ranges))
    axs3[1].set_ylim(bottom = -0.1, top = 1.0)
    axs3[1].set_xlabel("Spectrum index", fontsize = 12)
    axs3[1].set_ylabel("Reflectance range", fontsize = 12)
    axs3[1].set_title("{} spectra reflectance ranges".format(ext), fontsize = 15)
    
    plt.draw()
    
    

if __name__ == "__main__":
    asd_dir = "/home/pravindran/mycode/sdal_data/tests_data/test_GreenVegDetector/asd"
    sed_dir = "/home/pravindran/mycode/sdal_data/tests_data/test_GreenVegDetector/sed"
    
    test(asd_dir, 'asd')
    test(sed_dir, 'sed')
    plt.show()    