# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 15:51:32 2024

@author: (Jeremy)
"""

import tifffile
import numpy as np
import os
import re

def rename_tiff(output_filename, channel_list):
    for key, value in channel_list.items():
        output_filename = output_filename.replace(key, value)

    return output_filename

def process_tiff(tiff_path, output_dir, channel_list):

    splitted_tiffs = []

    # Isolates the xx_yy region from the file directory
    tiff_name = re.split(r'[/,.]', tiff_path)[-2]

    # Load the multi-channel, multi-z-plane TIFF file
    with tifffile.TiffFile(tiff_path) as tiff:
        images = tiff.asarray()  # Read the entire TIFF as a numpy array
        metadata = tiff.series[0].axes  # Get axes information

    if 'C' not in metadata or 'Z' not in metadata:
        raise ValueError("The TIFF file doesn't have channels or z-planes")

    # Get the number of channels and z-planes
    channel_idx = metadata.index('C')
    num_channels = images.shape[channel_idx]

    z_plane_idx = metadata.index('Z')
    num_z_planes = images.shape[z_plane_idx]

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Split and save each channel and z-plane: for manual toggling, if channel 4-6, then write 3-6.
    for c in range(num_channels):
        for z in range(num_z_planes):
            # Select the appropriate channel and z-plane
            single_image = images.take(c, axis=channel_idx).take(z, axis=z_plane_idx)
            
            # Save the image
            output_filename = f'c{c+1}_{tiff_name}_z{z+1}.tiff'
            new_output_filename = rename_tiff(output_filename, channel_list)
            output_path = os.path.join(output_dir, new_output_filename)
            tifffile.imwrite(output_path, single_image)
            
            # Saves file extension to a list
            output_path = output_path.replace('\\','/')
            splitted_tiffs.append(output_path)

    print(f"Saved {num_channels * num_z_planes} images to {output_dir}")

    return splitted_tiffs

def z_channels(tiff_path):

    # Load the multi-channel, multi-z-plane TIFF file
    with tifffile.TiffFile(tiff_path) as tif:
        images = tif.asarray()  # Read the entire TIFF as a numpy array
        metadata = tif.series[0].axes  # Get axes information

    if 'C' not in metadata or 'Z' not in metadata:
        raise ValueError("The TIFF file doesn't have channels or z-planes")

    z_plane_idx = metadata.index('Z')
    num_z_planes = images.shape[z_plane_idx]

    return num_z_planes