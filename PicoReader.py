# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 21:12:50 2015

@author: prabu
"""

from __future__ import print_function
import json
import os, os.path
import numpy as np
from helpers import get_directory_filename_extension
from Spectrum import Spectrum


class PicoReader:
    def __init__(self):
        pass
    
    def read(self, filename):
        d = json.loads(open(filename).read())
        num_spectra = len(d['Spectra'])
        idstr = get_directory_filename_extension(filename)[1]
        company = 'piccolo'
        instrument = 'piccolo'
        spectrums = []
        for i in range(num_spectra):
            #the metadata for the spectrum
            metadata = d['Spectra'][i]['Metadata']
            
            #processing the measurements (pixels)
            #read the pixel values
            pixels = np.array(d['Spectra'][i]['Pixels'], dtype = np.double)
#            print('pixels = {}'.format(pixels[-10:-1]))
            num_pixels = len(pixels)
            #get nonlinearity coefficients from metadata
            nlin_coeffs = np.array(metadata['NonlinearityCorrectionCoefficients'])
            #build pmat to contain [1, p, p^2, p^3, ...]
            pmat = np.ndarray((num_pixels, len(nlin_coeffs)), dtype = np.double)
            pmat[:, 0] = 1.0
            for c in range(1, len(nlin_coeffs)):
                pmat[:, c] = pmat[:, (c - 1)]*pixels
            #apply the nonlinearity coefficients
            pixels = np.dot(pmat, nlin_coeffs)
#            print('\n becomes \n')
#            print('pixels = {}'.format(pixels[-10:-1]))
#            print(nlin_coeffs)
            
            #processing the wavelengths
            #create a 0 start index list
            widxs = np.arange(0, num_pixels)
            #get wavelength polynomial coefficients from metadata
            wave_coeffs = np.array(metadata['WavelengthCalibrationCoefficients'])
            #build matrix that looks like [1, x, x^2, x^3, ....]
            wmat = np.ndarray((num_pixels, len(wave_coeffs)), dtype = np.double)
            wmat[:, 0] = 1
            for c in range(1, len(wave_coeffs)):
                wmat[:, c] = wmat[:, (c - 1)]*widxs
            #apply polynomial coefficients to get real wavelengths
            waves = np.dot(wmat, wave_coeffs)
            
            #create and append spectrum
            spectrums.append(Spectrum(data = np.column_stack((waves, pixels)), 
                                      idstr = idstr, 
                                      company = company,
                                      instrument = instrument,
                                      metadata = metadata))
#            print(===============================================\n\n")
        return spectrums
            
    
if __name__ == "__main__":
    print("PicoReader.py")
    
    d = '/home/prabu/mycode/sdal_data/tests_data/pico_test1/'
    f = os.path.join(d, '000001_v1_multiplespectrometers.pico')
#    f = os.path.join(d, '000007_v1_multiplespectrometers_no_dark.pico')
    
    pr = PicoReader()
    spectrums = pr.read(f)