# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 11:43:13 2015

@author: pravindran
"""

from __future__ import print_function
import os, os.path
import time
import shutil
from collections import defaultdict, namedtuple
import numpy as np
import matplotlib.pyplot as plt


 
SaveSpec = namedtuple('SaveSpec', 'group df plots specs means medians stds')

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
        if  smin > -0.1 and smax < 2.5:
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
def save_data(out_dir, 
              raw_white_specs, 
              raw_target_specs, 
              proc_target_specs,
              patt_name,
              patt_groups):
                  
    from SpectrumGroup import SpectrumGroup
    
    #create output directories   
    sodir = os.path.join(out_dir, 'sdal_outputs')
    if os.path.exists(sodir):
        shutil.rmtree(sodir)
        time.sleep(0.1)   
        print("  Deleted: {}".format(sodir))    
    os.mkdir(sodir)
    os.mkdir(os.path.join(sodir, 'raw_whites'))
    os.mkdir(os.path.join(sodir, 'raw_targets'))
    os.mkdir(os.path.join(sodir, 'proc_targets'))
    os.mkdir(os.path.join(sodir, 'plots'))
    os.mkdir(os.path.join(sodir, 'dataframes'))
    os.mkdir(os.path.join(sodir, patt_name + "_means"))
    os.mkdir(os.path.join(sodir, patt_name + "_medians"))                    
    os.mkdir(os.path.join(sodir, patt_name + "_stds"))
    print("   Created output directory sdal_outputs and its sub-directories")
    
    #create the list of namedtuples in order to save data and plots
    save_specs = []
    stat_groups = defaultdict(list)
    #construct named tuples for the patt_groups
    for g in patt_groups:
        ss = SaveSpec(group = g,
                      df = os.path.join(sodir, 'dataframes'),
                      plots = os.path.join(sodir, 'plots'),
                      specs = "",
                      means = os.path.join(sodir, patt_name + "_means"),
                      medians = os.path.join(sodir, patt_name + "_medians"),
                      stds = os.path.join(sodir, patt_name + "_stds"))
        save_specs.append(ss)              
        stat_groups['means'].append(g.mean)
        stat_groups['medians'].append(g.median)
        stat_groups['stds'].append(g.std)
    print("    Constructed SaveSpec for patt_groups")
    
    #construct a spectrum group and named tuple for the stat_groups spectrums
    for key in stat_groups:
        sg = SpectrumGroup().group(spectrums = stat_groups[key],
                                   group_name = patt_name + "_" + key)
        ss = SaveSpec(group = sg,
                      df = os.path.join(sodir, 'dataframes'),
                      plots = os.path.join(sodir, 'plots'),
                      specs = "", 
                      means = "", 
                      medians = "",
                      stds = "")
        save_specs.append(ss)
    print("    Constructed SaveSpec for stat_groups")
    #construct a spectrum group and named tuple for raw and proc spectrums
    raw_proc_groups = {'raw_whites': raw_white_specs,
                       'raw_targets': raw_target_specs, 
                       'proc_targets': proc_target_specs}
    for key in raw_proc_groups:
        sg = SpectrumGroup().group(spectrums = raw_proc_groups[key],
                                   group_name = key)
        ss = SaveSpec(group = sg,
                      df = os.path.join(sodir, 'dataframes'),
                      plots = os.path.join(sodir, 'plots'),
                      specs = os.path.join(sodir, key), 
                      means = "", 
                      medians = "",
                      stds = "")
        save_specs.append(ss)
    print("    Constructed SaveSpec for raw_proc_groups")
    #do the data output
    for ss in save_specs:
        if ss.group.is_empty():
            print("      EMPTY: {}".format(ss.group.name))
        else:
            ss.group.save_dataframe(ss.df)
            ss.group.save_plots(ss.plots)
            ss.group.save_spectrums(ss.specs)
            ss.group.save_stats(ss.means, ss.medians, ss.stds)
            print("      Saved: {}".format(ss.group.name))


#----------------------------------------------------------------------------    
if __name__ == "__main__":
    print("spectrum_utils.py")
    
    
#---------------------------------------------------------------------------
    
    