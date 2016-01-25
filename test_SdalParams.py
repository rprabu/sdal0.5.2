# -*- coding: utf-8 -*-
"""
Created on Tue May 19 15:20:18 2015

@author: prabu
"""

from __future__ import print_function
from SdalParams import SdalParams

if __name__ == "__main__":
    f = "/home/prabu/mycode/sdal/tests_data/test_SdalParams/params1.txt"
#    f = "/home/prabu/mycode/sdal/demo_data/params/demo1.txt"
    sp = SdalParams()
    sp.parse_file(f)
    sp.print_params()
    print("default_group = {}".format(sp.default_group))
    