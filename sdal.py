# -*- coding: utf-8 -*-
"""
Created on Tue May 19 16:48:14 2015

@author: prabu
"""

from __future__ import print_function
import os, os.path
import sys
from collections import defaultdict
from SdalReader import SdalReader
from SdalParams import SdalParams
from OverlapHandler import OverlapHandler
from WaveResampler import WaveResampler
from JumpCorrector import JumpCorrector
from SpectrumRegex import SpectrumRegex
from SpectrumGroup import SpectrumGroup
from WaveUniquifier import WaveUniquifier
from ReferenceDetector import ReferenceDetector
from helpers import get_directory_filename_extension


def process(params):
#    params.print_params()
    #get the project params and verify
    project = params.get_params("project")
    if project:
        verify_project(project)
    else:
        print("--project is required")
        sys.exit(0)
    #get the resampling params
    resampling = params.get_params("resampling")
    #get the jumpcorrection params and verify
    jumpcorrection = params.get_params("jumpcorrection")
    if jumpcorrection:
        verify_jumpcorrection(jumpcorrection)
    
    #get the groupings and verify them
    groupings = {grp:params.get_params(grp) for grp in params.get_groups()}
    verify_groupings(params.default_group, params.get_groups(), groupings)

    tags = ["raw", params.default_group]
    specs = defaultdict(list)
    #specs["raw"] created
    #get the filenames
    allfiles = os.listdir(project["indir"])
    extfiles = []
    for f in allfiles:
        ext = get_directory_filename_extension(f)[2]
        if ext == project["fileext"]:
            extfiles.append(os.path.join(project["indir"], f))
    #read the raw spectrums
    uniquifier = WaveUniquifier()
    rawspecs = [SdalReader().read_spectrum(f) for f in extfiles]
    uniqspecs = [uniquifier.uniquify(s) for s in rawspecs]
    specs["raw"] = uniqspecs
    
    #specs["preproc"] created
    #do the pre-processing
    prepspecs = specs["raw"]
    if resampling:
        resampler = WaveResampler(rstype = resampling["type"],
                                  wavestart = resampling["range"][0],
                                  wavestop = resampling["range"][1],
                                  spacing = resampling["spacing"])
        rsspecs = [resampler.resample(s) for s in prepspecs]
        prepspecs = rsspecs
    if jumpcorrection:
        corrector = JumpCorrector(jumpcorrection["wavelengths"],
                                  jumpcorrection["stablezone"])
        jcspecs = [corrector.correct(s) for s in prepspecs]
        prepspecs = jcspecs
    #detect the references
    refdet = ReferenceDetector(context = "gveg")
    nonrefs = []
    refs = []
    for s in prepspecs:
        if refdet.is_reference(s):
            refs.append(s)
        else:
            nonrefs.append(s)
    specs[params.default_group] = nonrefs
    
    #specs[group_tag] created
    #do the grouping 
    for t in groupings:
        tags.append(t)
        itag = groupings[t]["intag"]
        patt = groupings[t]["pattern"]
        regex = SpectrumRegex()
        tgrps = regex.make_groups(specs[itag], patt)
        for tg in tgrps:
            sg = SpectrumGroup(spectrums = tgrps[tg])
            ms = sg.mean_spectrum()
            ms.idstr = tg
            specs[t].append(ms)

#    subsets = {grp:params.get_params(grp) for grp in params.get_subsets()}
#    print(subsets)
#    for t in subsets:
#        itag = subsets[t]["intag"]
#        otag = subsets[t]["outtag"]
#        wavestart = subsets[t]["range"][0]
#        wavestop = subsets[t]["range"][1]
#        for s in specs[itag]:
#            subspec = s.wavelength_subset(wavestart, wavestop)
#            subspec.idstr = subspec.idstr + otag
#            print("idstr = {}".format(subspec.idstr))
#            specs[otag].append(subspec)
                           
    #create outputs
    prjdir = os.path.join(project["outdir"], project["name"])
    os.mkdir(prjdir)
    for t in specs:
        tdir = os.path.join(prjdir, t)
        os.mkdir(tdir)
        tgrpfn = "___{}___.csv".format(t)                       
        for s in specs[t]:
            s.write_csv(odir = tdir)
        sg = SpectrumGroup(spectrums = specs[t])
        sg.write_csv(tdir, tgrpfn)
                        
                        
                        
                        
def verify_groupings(default, grouptags, groupings):
    availtags = [default]
    for g in grouptags:
        intag = groupings[g]["intag"]
        if intag not in availtags:
            print("-intag for grouping: {} is invalid".format(intag))
            sys.exit(0)
        availtags.append(groupings[g]["outtag"])
    

def verify_jumpcorrection(jumpcorrection):
    status = True
    msgs = ["--jumpcorrection parameters"]
    numzones = len(jumpcorrection["wavelengths"]) + 1
    zoneidx = jumpcorrection["stablezone"]
    if zoneidx >= numzones:
        status = False
        tmplt = "stablezone: {} not less than numzones: {}"
        msgs.append(tmplt.format(zoneidx, numzones))
    if not status:
        print("\n".join(msgs))
        sys.exit(0)

    
def verify_project(project):
    status = True
    msgs = ["--project parameters"]
    #check validity of input directory
    idir = project["indir"]
    if not os.path.exists(idir) or not os.path.isdir(idir):
        status = False
        msgs.append("Invalid input directory: {}".format(idir))
    #check output directories
    odir = project["outdir"]
    pdir = os.path.join(odir, project["name"])
    if not os.path.exists(odir) or not os.path.isdir(odir):
        status = False
        msgs.append("Invalid output directory: {}".format(odir))
    if os.path.exists(pdir):
        status = False
        msgs.append("Project directory already exists".format(pdir))
    if not status:
        print("\n".join(msgs))
        sys.exit(0)


def from_paramfile(args):
    params = SdalParams()
    params.parse_file(args[1])
    return params

def from_commandline(args):
    pass


def missing_message(tag, reqd, found):
    print("Missing parameters for --{}".format(tag))
    
    
if __name__ == "__main__":
    print("SDAL processing")

#    args = ["--paramsfile",
#            "/home/prabu/mycode/sdal/demo_data/params/demo1.txt"]
#    process(from_paramfile(args))
        
    if "--paramsfile" in sys.argv[1:] or "--paramfile" in sys.argv[1:]:
        process(from_paramfile(sys.argv[1:]))
    else:
        process(from_commandline(sys.argv[1:]))
        