#TO SOLVE: issue of bleach (perhaps we just iterate over every 2nd file. Or we just set manual hyb numbers...)
# TO SOLVE: adjusting the file rename (don't do the rename before, do it after...)
# TO SOLVE: have an option for toggling between tiff and dax. I think its quite bad if we save both

import os
import tkinter as tk
import glob
import re
import shutil
from tkinter import filedialog

from imstotiff import driver
from tiffprocessing import process_tiff, z_channels
from tifftodax import create_dax

# PARAMETERS TO MODIFY #
# channel_list = {"c1": "Cy3_WF", "c2": "Cy7_WF", "c3": "Cy5_WF", "c4": "Cy3_confocal", "c5": "Cy7_confocal", "c6": "Cy5_confocal"}
channel_list = {"c1": "Cy3", "c2": "Cy5"}
save_as_dax = True # Set to false to save as tiff



# Select directory containing .ims / .tiff files
root = tk.Tk()
root.withdraw()
data_path = filedialog.askdirectory(title="Please select data directory")
root.destroy()


#Converts ims to tiff (NOTE: The Oakes lab code saves it as .tif and the below uses .tiff which is quite amusing)
    
# Get all of the ims files
cwd = data_path + '/'
ims_files = glob.glob(cwd + '*.ims')
ims_files = [f_name.replace('\\','/' ) for f_name in ims_files]

# Pass the filenames and the downsample factor to the driver
driver(ims_files, ds_factor = 1)

# Renames tiff files
# Iterate through all files in the directory
for filename in os.listdir(data_path):
    _, ext = os.path.splitext(filename)
    if ext == ".tiff":
        # Split the filename to extract the part with the pattern like "2_F00"
        parts = filename.split('_')
        # For cases where the file ends with "Sona_F00" which indicates the first hyb. This corresponds to 00_00 on Dory (should be more dynamic)
        if parts[-2].startswith('Sona'):
            # Assumes that DAPI images are taken on first hyb and named separately from the first hyb (filename starts with DAPI)
            if parts[1].startswith('DAPI'):
                new_filename = f'DAPI_00_0{parts[-1][1:]}'
                break  
            new_filename= f'00_0{parts[-1][1:]}'
        else:
            new_filename = f'{parts[-2].zfill(2)}_0{parts[-1][1:]}'
        
        # Construct the full old and new file paths
        old_file_path = os.path.join(data_path, filename)
        new_file_path = os.path.join(data_path, new_filename)
        
        # Rename the file
        os.rename(old_file_path, new_file_path)
        print(f'Renamed: {old_file_path} -> {new_file_path}')


# Grabs all tiff files
tiff_files = glob.glob(cwd + '*.tiff')

# Obtains number of z stacks in each tiff image. It looks only at the first tiff image which is assumed to be the same format as the rest.
z_number = z_channels(tiff_files[0])

# Prepares folders to slot images into later.
for z_current in range(z_number):
    folder_name = f'zstack_{z_current + 1}'
    folder_path = os.path.join(cwd, folder_name)
    os.makedirs(folder_path, exist_ok=True)

# Splits and appends channels to file name. The logic should be correct
for tiff in tiff_files:
    tiff = tiff.replace('\\','/' )
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
        
        # # Ensure the destination folder exists
        os.makedirs(dest_folder, exist_ok=True)
        
        # Move the file to the corresponding folder
        src_file = os.path.join(cwd, file)
        dest_file = os.path.join(dest_folder, file)
        shutil.move(src_file, dest_file)