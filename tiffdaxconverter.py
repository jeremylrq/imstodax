#!/usr/bin/env python
"""
Performs file conversions (code from Zhuang lab)
"""
import sa_library.datawriter as datawriter
import sa_library.datareader as datareader
import tkinter as tk
import glob
import os
from tkinter import filedialog


def create_dax(splitted_tiffs):
     for tiff in splitted_tiffs:
          dax_file = datawriter.DaxWriter(tiff.replace('.tiff', '.dax'))
          data = datareader.TifReader(tiff).loadAFrame(0)
          dax_file.addFrame(data)
          dax_file.close()

def create_tiff(dax_files):
     for dax in dax_files:
          tiff = datawriter.TiffWriter(dax.replace('.dax', '.tiff'))
          data = datareader.DaxReader(dax).loadAFrame(0)
          tiff.addFrame(data)
          tiff.close()


# The main script chooses dax-tiff or tiff-dax conversion. Performs conversion for entire directory (leaving original file intact)

if __name__ == "__main__":
     
     dax_to_tiff = False
     tiff_to_dax = False
     
     # Select directory containing .ims / .tiff files
     root = tk.Tk()
     root.withdraw()
     data_path = filedialog.askdirectory(title="Please select data directory")
     root.destroy()
     cwd = data_path + '/'
     
     while True:
          converter = input("0 if converting from tiff to dax, 1 if converting from dax to tiff")
          if converter == "1":
                dax_to_tiff = True
                break
          elif converter == "0":
                tiff_to_dax = True
                break
          else:
                print("Enter valid input")
     
     if dax_to_tiff:
          dax_files = glob.glob(cwd + '*.dax')
          dax_files = [d_name.replace('\\','/') for d_name in dax_files]

          create_tiff(dax_files)

     if tiff_to_dax:
          # Bulk rename .tif to .tiff as tifffile only recognises .tiff
          tif_files = glob.glob(cwd + '*.tif')

          for file in tif_files:
               new_file_path = file.replace(".tif", ".tiff")
               os.rename(file, new_file_path)

          tiff_files = glob.glob(cwd + '*.tiff')
          tiff_files = [t_name.replace('\\','/') for t_name in tiff_files]

          create_dax(tiff_files)

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
