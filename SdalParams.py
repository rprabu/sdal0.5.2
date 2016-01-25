# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 22:10:11 2015

@author: prabu
"""


from __future__ import print_function
import sys
import argparse


class SdalParams:

    #------------------------------------------------------------------------    
    def __init__(self):
        self._params = {}

    
    #------------------------------------------------------------------------                      
    def parse_file_townsend_asd_processing(self, paramfile):
        try:
            #read the lines from the parameter file
            rawlines = []
            with open(paramfile, 'r') as f:
                rawlines = f.readlines()
            
            #extract non-empty lines
            nonemptylines = [l.strip() for l in rawlines if l.strip()]
            
            #extract non-comment lines
            noncommentlines = [l for l in nonemptylines if l[0] != '#']

            #get words from the lines    
            alltkns = " ".join(noncommentlines).split()
            
            #use argparse to ge the params           
            #setup a parser
            par = argparse.ArgumentParser(description = "paramfile parser")
            par.add_argument("--project_name",
                             type = str,
                             required = True,
                             dest = "project_name")
            par.add_argument("--project_input_directory",
                             type = str,
                             required = True,
                             dest = "project_input_directory")
            par.add_argument("--project_output_directory",
                             type = str,
                             required = True,
                             dest = "project_output_directory")
            par.add_argument("--project_file_extension",
                             type = str,
                             required = True,
                             dest = "project_file_extension")
            par.add_argument("--subset_wavelength_range",
                             type = float,
                             nargs = 2,
                             required = True,
                             dest = "subset_wavelength_range")
            par.add_argument("--jumpcorrection_wavelengths",
                             type = float,
                             nargs = 2,
                             required = True,
                             dest = "jumpcorrection_wavelengths")
            par.add_argument("--jumpcorrection_stablezone",
                             type = int,
                             required = True,
                             dest = "jumpcorrection_stablezone")
            par.add_argument("--grouping_output_name",
                             type = str,
                             required = True,
                             dest = "grouping_output_name")
            par.add_argument("--grouping_pattern",
                             type = str,
                             required = True,
                             dest = "grouping_pattern")
            
            #parse it
            self._params = par.parse_known_args(alltkns)[0].__dict__

            #verify everything is correctly specified
            self._verify_townsend_asd_processing()
            
        except IOError:
            print("Invalid parameter file: {}".format(paramfile))
            sys.exit(0) 
    

    #------------------------------------------------------------------------    
    def _verify_townsend_asd_processing(self):
        pass
    
    
    #------------------------------------------------------------------------
    def parse_file_old(self, paramfile):
        try:
            rawlines = []
            with open(paramfile, 'r') as f:
                rawlines = f.readlines()
            nelines = [l for l in rawlines if l.strip()]
            nclines = [l.strip() for l in nelines if l[0] != self._comment]
            lines = " ".join(nclines)
            alltkns = lines.split()
            #IMPORTANT: Persist with this way of doing the parsing
            #We need to maintain the order in which groupings were 
            #presented in the parameter list inorder to verify that
            #the groupings parameters are valid. We use the new tags
            #that are created in order to verify validity of grouping.
            idxs = [i for (i, t) in enumerate(alltkns) if t in self._mapper]
            idxs.append(len(alltkns))
            for i in range(1, len(idxs)):
                tag = alltkns[idxs[i - 1]]
                tkns = alltkns[(idxs[i - 1] + 1) : idxs[i]]
                (tagkey, keyvals, partype) = self._mapper[tag](tkns)
                self._params[tagkey] = keyvals
                if partype == "grouping":
                    self._groups.append(tagkey)
                elif partype == "subsetting":
                    self._subsets.append(tagkey)
        except IOError:
            print("Invalid parameter file: {}".format(paramfile))
            sys.exit(0)   

    
    def parse_cli(self, argtkns):
        idxs = [i for (i, t) in enumerate(argtkns) if t in self._mapper]
        idxs.append(len(argtkns))
        for i in range(1, len(idxs)):
            tag = argtkns[idxs[i - 1]]
            tkns = argtkns[(idxs[i - 1] + 1) : idxs[i]]
            (tagkey, keyvals, partype) = self._mapper[tag](tkns)
            self._params[tagkey] = keyvals
            if partype == "grouping":
                self._groups.append(tagkey)
    
    
    def _resampling_params(self, l):
        tag, keyvals = "resampling", {}
        par = argparse.ArgumentParser(description = "--resampling")
        par.add_argument("-range",
                         type = float,
                         nargs = 2,
                         required = True)
        par.add_argument("-spacing", 
                         type = float,
                         required = True)
        par.add_argument("-type", 
                         type = str, 
                         choices = ('cubic', 'linear'),
                         required = True)
        try:        
            keyvals = par.parse_known_args(l)[0].__dict__
            return (tag, keyvals, "processing")
        except:
            par.print_help()
            sys.exit(0)

    
    def _jumpcorrection_params(self, l):
        tag, keyvals = "jumpcorrection", {}
        par = argparse.ArgumentParser(description = "--jumpcorrection")
        par.add_argument("-wavelengths", 
                         type = float, 
                         nargs = '+',
                         required = True)
        par.add_argument("-stablezone", 
                         type = int,
                         required = True)
        par.add_argument("-maxjump", 
                         type = float, 
                         required = True)
        try:        
            keyvals = par.parse_known_args(l)[0].__dict__
            return (tag, keyvals, "processing")
        except:
            par.print_help()
            sys.exit(0)

       
    def _grouping_params(self, l):
        keyvals = {}
        par = argparse.ArgumentParser(description = "--grouping")
        par.add_argument("-intag", 
                         type = str,
                         required = True)
        par.add_argument("-outtag", 
                         type = str,
                         required = True)
        par.add_argument("-pattern", 
                         type = str,
                         required = True)
#        par.add_argument("-dfname", 
#                         type = str,
#                         required = True)
        try:
            keyvals = par.parse_known_args(l)[0].__dict__
            return (keyvals["outtag"], keyvals, "grouping")
        except:
            par.print_help()
            sys.exit(0)


    def _subsetting_params(self, l):
        keyvals = {}
        par = argparse.ArgumentParser(description = "--subsetting")
        par.add_argument("-intag", 
                         type = str,
                         required = True)
        par.add_argument("-outtag", 
                         type = str,
                         required = True)
        par.add_argument("-range",
                         type = float,
                         nargs = 2,
                         required = True)

        try:
            keyvals = par.parse_known_args(l)[0].__dict__
            return (keyvals["outtag"], keyvals, "subsetting")
        except:
            par.print_help()
            sys.exit(0)
    
    
    def _project_params(self, l):
        tag, keyvals = "project", {}
        par = argparse.ArgumentParser(description = "--project")
        par.add_argument("-indir", 
                         type = str,
                         required = True)
        par.add_argument("-outdir", 
                         type = str,
                         required = True)
        par.add_argument("-name", 
                         type = str,
                         required = True)
        par.add_argument("-fileext", 
                         type = str,
                         required = True)
        par.add_argument("-dfname", 
                         type = str,
                         required = True)
        try:        
            keyvals = par.parse_known_args(l)[0].__dict__
            return (tag, keyvals, "project")
        except:
            par.print_help()
            sys.exit(0)
    
    
    @property
    def default_group(self):
        return self._default_group
        
        
    def get_groups(self):
        return self._groups
        
    
    def get_subsets(self):
        return self._subsets

        
    def get_params(self, tag):
        try:
            return self._params[tag]
        except KeyError:
            return {}
            
    @property
    def params(self):
        return self._params
            
            
    def print_params(self):
        print("params = \n {}".format(self._params))
        print("groups = {}".format(self._groups))
        print("subsets = {}".format(self._subsets))
        
    
if __name__ == "__main__":
    print("SdalParams.py")
    
    