# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 15:51:32 2024

@author: (Jeremy)
"""

import os
import tkinter as tk
import glob
import re
import shutil
import math
from math import floor, ceil
from tkinter import filedialog

from imstotiff import driver
from tiffprocessing import process_tiff
from tiffdaxconverter import create_dax

################### PARAMETERS TO MODIFY MANUALLY ##########################
# channel_list = {"c1": "Cy3_WF", "c2": "Cy7_WF", "c3": "Cy5_WF", "c4": "Cy3_confocal", "c5": "Cy7_confocal", "c6": "Cy5_confocal"}
# channel_list = {"c1": "Cy3", "c2": "Cy5"} # Set the channel labels
channel_list = {"c4": "Cy3", "c5": "Cy7", "c6": "Cy5"} # Set the channel labels

save_as_dax = True # Set to false to save as tiff
remove_z_label = True # To remove trailing z at the back of filename
bleach = True # Set true/false to toggle bleach numbering

# Check files to toggle first and final hyb numbers manually. Must be integers. The first hyb number must be a hyb round and not a bleaching round.
first_hybnum = 0
last_hybnum = 5
####################################################################

# Select directory containing .ims / .tiff files
root = tk.Tk()
root.withdraw()
data_path = filedialog.askdirectory(title="Please select data directory")
root.destroy()

#Converts ims to tiff
    
# Get all of the ims files
cwd = data_path + '/'
ims_files = glob.glob(cwd + '*.ims')
ims_files = [f_name.replace('\\','/' ) for f_name in ims_files]

# Pass the filenames and the downsample factor to the driver. Code has been modified to return a list of all .tiff files 
tiff_files = driver(ims_files, ds_factor = 1)

renamed_tiff_files = []

if bleach:       
    if first_hybnum > last_hybnum:
        print("The first hyb number is larger than the final hyb number. Please input valid hyb numbers.")
        exit(0)
    
    # Produces a dictionary mapping the numbers in the file to the actual hyb number
    if first_hybnum % 2 == 0:
        print("First hyb number is even. Hyb rounds 0, 2, 4, etc... will be set as normal hybs.")
        print("Hyb numbers 1, 3, 5... will be set as bleach rounds.")
        evenhybs = True

    else:
        print("First hyb number is odd. Hyb rounds 1, 3, 5, etc... will be set as normal hybs.")
        print("Hyb numbers 2, 4, 6... will be set as bleach rounds.")
        evenhybs = False

    hybmap = {}
    for i in range(first_hybnum, last_hybnum + 1):  # Adjust the range as needed
        # Avoid divisibility errors
        if i == 0:
            hybmap[0] = 0
        else:
            if evenhybs:
                hybmap[i] = floor(i/2)

            elif not evenhybs:
                hybmap[i] = ceil(i/2)

# This renames the file and outputs a filename of the format e.g. 00_01.tiff
for file in tiff_files:
    parts = re.split(r'[_\.]', file)
    
    # For cases where the file ends with "Sona_F00" which indicates the first hyb. This corresponds to 00_00 on Dory (should be more dynamic)
    #  if parts[-3].startswith('Sona'):
    #     # Assumes that DAPI images are taken on first hyb and named separately from the first hyb (filename starts with DAPI)
    #     if parts[1].startswith('DAPI'):
    #         new_filename = f'DAPI_00_0{parts[-2][1:]}'
    #         break  
    #     # new_filename= f'00_0{parts[-2][1:]}'
    # else:
    hybvalue = int(parts[-3])

    if bleach:
        if evenhybs:
            if hybvalue % 2 == 0:
                hybvalue = hybmap[hybvalue] if hybvalue in hybmap else hybvalue
                new_filename = f'{str(hybvalue).zfill(2)}_{str(parts[-2][1:]).zfill(3)}.tiff'

            else:
                hybvalue = hybmap[hybvalue] if hybvalue in hybmap else hybvalue
                new_filename = f'Bleach_{str(hybvalue).zfill(2)}_{str(parts[-2][1:]).zfill(3)}.tiff'

        elif not evenhybs:
            if hybvalue % 2 == 0:
                hybvalue = hybmap[hybvalue] if hybvalue in hybmap else hybvalue
                new_filename = f'Bleach_{str(hybvalue).zfill(2)}_{str(parts[-2][1:]).zfill(3)}.tiff'

            else:
                hybvalue = hybmap[hybvalue] if hybvalue in hybmap else hybvalue
                new_filename = f'{str(hybvalue).zfill(2)}_{str(parts[-2][1:]).zfill(3)}.tiff'

        else:
            new_filename = f'{str(hybvalue).zfill(2)}_{str(parts[-2][1:]).zfill(3)}.tiff'

    
    new_file_path = os.path.join(cwd, new_filename)
        
    os.rename(file, new_file_path)
    print(f'Renamed: {file} -> {new_file_path}')
    renamed_tiff_files.append(new_file_path)

# Splits and appends channels to file name. 
for tiff in renamed_tiff_files:
    tiff = tiff.replace('\\','/')
    splitted_tiffs = process_tiff(tiff, data_path, channel_list)

    if save_as_dax:
        create_dax(splitted_tiffs)
    else:
        continue

# Sorts all files into their z stack

# Get a list of all files in the directory
files = os.listdir(cwd)

# Loop through each file
for file in files:
    
    _ , ext = os.path.splitext(file)
    
    # Deletes tiff files 
    if save_as_dax:
        if ext == ".tiff":
            file_h = cwd + file
            os.remove(file_h)
            continue

    # Check if the file matches the expected pattern with z-index
    match = re.search(r'_z(\d+)', file)
    
    if match:
        # Extract the z-index from the filename
        z_index = int(match.group(1))
        
        # Construct the corresponding folder name
        folder_name = f'zstack_{z_index}'
        
        # Define the full path to the destination folder
        dest_folder = os.path.join(cwd, folder_name)
        
        # Ensure the destination folder exists
        os.makedirs(dest_folder, exist_ok=True)
        
        # Move the file to the corresponding folder.

        if remove_z_label:
            file_path = cwd + file
            new_file_path = file_path.replace(f'_z{z_index}', '')
            os.rename(file_path, new_file_path)

            src_file = new_file_path
            dest_file = os.path.join(dest_folder, os.path.basename(src_file))

        else:
            src_file = os.path.join(cwd, file)
            dest_file = os.path.join(dest_folder, file)

        shutil.move(src_file, dest_file)
