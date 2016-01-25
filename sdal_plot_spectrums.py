# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 11:43:13 2015

@author: pravindran
"""

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt


def plot_spectrums(spectrums,
                   spectrums_color,
                   title,
                   stat_spectrum = None,
                   stat_spectrum_color = None):
    
    plt.close()               
    #find the min and maxwaves in the spectrums
    #this will be used to set the xlim for plots
    minwaves = []
    maxwaves = []
    for s in spectrums:
        minwaves.append(s.wavelengths[0])
        maxwaves.append(s.wavelengths[-1])
    if stat_spectrum:
        minwaves.append(stat_spectrum.wavelengths[0])
        maxwaves.append(stat_spectrum.wavelengths[-1])
    minwave = min(minwaves)
    maxwave = max(maxwaves)
    
    #plot the spectrums
    numbad = 0
    fig, ax = plt.subplots()
    for s in spectrums:
        smin = np.min(s.reflectances)
        smax = np.max(s.reflectances)
        if  smin > -0.5 and smax < 2.5:
            ax.plot(s.wavelengths, s.reflectances, color = spectrums_color)
        else:
            numbad += 1
            print("{}: Not plotting {}, range: {}, {}".format(numbad,
                                                              s.idstr, 
                                                              smin, 
                                                              smax))

    #plot the stat_spectrum is provided                                            
    if stat_spectrum and stat_spectrum_color:
        ax.plot(stat_spectrum.wavelengths, 
                 stat_spectrum.reflectances,
                 color = stat_spectrum_color)
                 
    #some plot parameters
    ax.set_xlabel("Wavelengths")
    ax.set_ylabel("Reflectances")
    ax.set_xlim([minwave - 10, maxwave + 10])
    fig.suptitle(title)
    
    return fig



#----------------------------------------------------------------------------    
if __name__ == "__main__":
    print("sdal_plot_spectrums.py")
    
    
#---------------------------------------------------------------------------
    
    