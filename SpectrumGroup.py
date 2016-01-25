# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 15:13:34 2015

@author: prabu
"""

from __future__ import print_function
import sys
import os, os.path
import numpy as np
import pandas as pd
from Spectrum import Spectrum
from sdal_plot_spectrums import plot_spectrums

class SpectrumGroup:

    #------------------------------------------------------------------------    
    def __init__(self):
        self._waves = np.array([])
        self._refls = np.array([])
        self._idstrs = []    
        self._companys = []
        self._instruments = []
        self._name = ""
        
    
    #------------------------------------------------------------------------
    def group(self, spectrums, group_name):
        
        #input spectrums must not be empty
        if not spectrums:
            self._name = group_name
            return self
            
#        print("\tgroup_name = {}".format(group_name))
#        print("\tnum spectrums = {}".format(len(spectrums)))
#        for s in spectrums:
#            print("\t\tfile: {}".format(s.idstr))
#            print("\t\t: {} - {}".format(s.wavelengths[0], s.wavelengths[-1]))
    
        #check all spectrums have same wavelengths
        w0 = spectrums[0].wavelengths
#        r0 = spectrums[0].reflectances
#        print(len(spectrums[0].wavelengths))
#        for i in range(1,len(w0)):
#            if abs(w0[i] - w0[i - 1]) < 0.1:
#                print("same wave: {} {}".format(w0[i], w0[i-1]))
#                print("same refl: {} {}".format(r0[i], r0[i-1]))
        if not np.all([np.allclose(w0, s.wavelengths) for s in spectrums]):
            print("spectrums must have same wavelengths")
            sys.exit(0)
        
        #collect the data
        self._waves = np.copy(spectrums[0].wavelengths)
        nspectra, nwaves = len(spectrums), np.size(self._waves)
        self._refls = np.empty((nspectra, nwaves), dtype = np.double)
        for (i, s) in enumerate(spectrums):
            self._refls[i, :] = np.copy(s.reflectances.transpose())
            self._idstrs.append(s.idstr)
            self._companys.append(s.company)
            self._instruments.append(s.instrument)
        self._name = group_name
        
        return self
        
    
    #------------------------------------------------------------------------
    def save_dataframe(self, out_dir):
        #create default data frame from numpy array
        df = pd.DataFrame(self._refls)
        #make the columns names = wavelengths
        df.columns = [str(w) for w in self._waves]
        #introduce columns for idstrs, companies, instruments
        df.insert(0, "idstr", self._idstrs)
        df.to_csv(os.path.join(out_dir, self._name + "_df.csv"), 
                  index = False,
                  float_format = "%0.4f")
            
    
    #------------------------------------------------------------------------
    def save_plots(self, pdf_dir, png_dir):
        #create spectrum list
        spectrums = []
        for i in range(self._refls.shape[0]):
            dm = np.vstack((self._waves, self._refls[i, :])).transpose()
            spectrums.append(Spectrum(data = dm))
        
        #plot spectrums and save
        fig1_title = self._name
        fig1 = plot_spectrums(spectrums,
                              spectrums_color = 'cyan',
                              title = fig1_title)
        fig1.savefig(os.path.join(pdf_dir, fig1_title + ".pdf"))
        fig1.savefig(os.path.join(png_dir, fig1_title + ".png"))
        
        #plot spectrums + mean and save
        fig2_title = self._name + "_with_mean"
        fig2 = plot_spectrums(spectrums,
                              spectrums_color = 'cyan',
                              title = fig2_title, 
                              stat_spectrum = self.mean,
                              stat_spectrum_color = 'black')
        fig2.savefig(os.path.join(pdf_dir, fig2_title + ".pdf"))
        fig2.savefig(os.path.join(png_dir, fig2_title + ".png"))
        
        #plot spectrums + median and save
        fig3_title = self._name + "_with_median"
        fig3 = plot_spectrums(spectrums,
                              spectrums_color = 'cyan',
                              title = fig3_title, 
                              stat_spectrum = self.median,
                              stat_spectrum_color = 'black')
        fig3.savefig(os.path.join(pdf_dir, fig3_title + ".pdf"))
        fig3.savefig(os.path.join(png_dir, fig3_title + ".png"))    
    
    #------------------------------------------------------------------------
    def save_stats(self, mean_dir, median_dir, std_dir):
        if mean_dir: self.mean.write_csv(mean_dir)
        if median_dir: self.median.write_csv(median_dir) 
        if std_dir: self.std.write_csv(std_dir)  

    
    #------------------------------------------------------------------------
    def save_spectrums(self, out_dir):
        if not out_dir or np.size(self._waves) == 0:
            return
        for i in range(self._refls.shape[0]):
            dm = np.vstack((self._waves, self._refls[i, :])).transpose()
            Spectrum(data = dm, 
                     idstr = self._idstrs[i],
                     company = self._companys[i],
                     instrument = self._instruments[i]).write_csv(out_dir)
                     

    #------------------------------------------------------------------------
    def is_empty(self):
        return np.size(self._waves) == 0 or np.size(self._refls) == 0
        
        
    #------------------------------------------------------------------------
    @property
    def mean(self):
        means = np.mean(self._refls, axis = 0)
        dm = np.vstack((self._waves, means)).transpose()
        return Spectrum(data = dm, 
                        idstr = self._name + "_mean",
                        company = "NA",
                        instrument = "NA")

    
    #------------------------------------------------------------------------
    @property
    def std(self):
        stds = np.std(self._refls, axis = 0)
        dm = np.vstack((self._waves, stds)).transpose()
        return Spectrum(data = dm, 
                        idstr = self._name + "_std",
                        company = "NA",
                        instrument = "NA")


    #------------------------------------------------------------------------    
    @property
    def median(self):
        medians = np.median(self._refls, axis = 0)
        dm = np.vstack((self._waves, medians)).transpose()
        return Spectrum(data = dm, 
                        idstr = self._name + "_median",
                        company = "NA",
                        instrument = "NA")


    #------------------------------------------------------------------------    
    @property
    def name(self):
        return self._name
        
    

#------------------------------------------------------------------------    
if __name__ == "__main__":
    print("SpectrumGroup.py")
    