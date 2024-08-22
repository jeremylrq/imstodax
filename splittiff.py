import tifffile
import numpy as np
import os
import re

def process_tiff(tiff_path, output_dir, channel_list):

    # Isolates the xx_yy region from the file directory
    tiff_name = re.split(r'[/,.]', tiff_path)[-2]
    # print(f'This is the tiff_name', tiff_name)

    # Load the multi-channel, multi-z-plane TIFF file
    with tifffile.TiffFile(tiff_path) as tif:
        images = tif.asarray()  # Read the entire TIFF as a numpy array
        metadata = tif.series[0].axes  # Get axes information

    if 'C' not in metadata or 'Z' not in metadata:
        raise ValueError("The TIFF file doesn't have channels or z-planes")

    # Get the number of channels and z-planes
    channel_idx = metadata.index('C')
    num_channels = images.shape[channel_idx]

    z_plane_idx = metadata.index('Z')
    num_z_planes = images.shape[z_plane_idx]

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Split and save each channel and z-plane
    for c in range(num_channels):
        for z in range(num_z_planes):
            # Select the appropriate channel and z-plane
            single_image = images.take(c, axis=channel_idx).take(z, axis=z_plane_idx)
            # Save the image

            output_filename = f'c{c+1}_{tiff_name}_z{z+1}.tiff'
            new_output_filename = rename_tiff(output_filename, channel_list)

            output_path = os.path.join(output_dir, new_output_filename)
            tifffile.imwrite(output_path, single_image)

            # Renames the file to the conventional format (e.g. Cy3_00_01.tif)



    print(f"Saved {num_channels * num_z_planes} images to {output_dir}")
# # Usage example:
# tiff_path = 'OneDrive\\Desktop\\GIS attachment\\confocal testing\\test.tif'
# output_dir = 'C:\\Users\\Jeremy\\OneDrive\\Desktop\\GIS attachment\\confocal testing\\output'
# split_tiff(tiff_path, output_dir)



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

def rename_tiff(output_filename, channel_list):
    for key, value in channel_list.items():
        output_filename = output_filename.replace(key, value)

    return output_filename



if __name__ == "__main__":
    print(channels("C:\\Users\\Jeremy\\OneDrive\\Desktop\\GIS attachment\\confocal testing\\rename_test\\02_00000000000.tif"))