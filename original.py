#!/usr/bin/env python
"""
Convert a mess of tiff files into a single dax file.

Hazen 09/14
"""

import glob
import numpy
import sys
import os
import glob
import re

import sa_library.datawriter as datawriter
import sa_library.datareader as datareader

def create_dax(cwd, tiff_path):

     # First obtain the name of the tiff file
     tiff_name = re.split(r'[/,.]', tiff_path)[-2]
     dax_file = datawriter.DaxWriter(os.path.join(cwd + tiff_name + ".dax"))

     data = datareader.TifReader(tiff_path).loadAFrame(0)
     dax_file.addFrame(data)
     dax_file.close()


if __name__ == "__main__":
     create_dax()

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
