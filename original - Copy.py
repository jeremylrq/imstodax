#!/usr/bin/env python
"""
Convert a mess of tiff files into a single dax file.

Hazen 09/14
"""

import glob
import numpy
import sys
import os

import sa_library.datawriter as datawriter
import sa_library.datareader as datareader

# if (len(sys.argv) != 3):
#     print("usage: <dax> <tiff dir>")
#     exit()

#how do we know it is actually accessing the location???
#add2 is the one that works.

# dax_file = datawriter.DaxWriter(sys.argv[1])
dax_file = datawriter.DaxWriter("C:\\Users\\Jeremy\\OneDrive\\Desktop\\GIS attachment\\confocal testing\\output\\test\\test.dax")

# tiff_files = sorted(glob.glob(sys.argv[2]))

# tiff_files_add = sorted(glob.glob(sys.argv[2] + "*.tiff"))
# tiff_files_add2 = sorted(glob.glob(os.path.join(sys.argv[2], "*.tiff")))
tiff_files_add2 = sorted(glob.glob(os.path.join('C:\\Users\\Jeremy\\OneDrive\\Desktop\\GIS attachment\\confocal testing\\output\\test', "*.tiff")))



print("=====================================\n\n\n\n")

# print(tiff_files)
# print(tiff_files_add)
print(tiff_files_add2)



print("=====================================\n\n\n\n")

# if (len(tiff_files_add2) == 0):
#     print("No tiff files found in '" + sys.argv[2] + "'")
#     exit()

if (len(tiff_files_add2) == 0):
     print("No tiff files found in")
     exit()

for tiff_image in tiff_files_add2:
    print(tiff_image)

    #seems like its able to read the tiff (set Verbose = true)
    data = datareader.TifReader(tiff_image).loadAFrame(0)
    print(data)

    #I think this seems to do nothing.
    if 0:
         data = data - numpy.median(data) + 2000
    dax_file.addFrame(data)

dax_file.close()

#
# The MIT License
#
# Copyright (c) 2014 Zhuang Lab, Harvard University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
