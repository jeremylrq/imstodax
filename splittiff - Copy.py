import tifffile
import numpy as np
import os

def split_tiff(tiff_path, output_dir):
    # Load the multi-channel, multi-z-plane TIFF file
    with tifffile.TiffFile(tiff_path) as tif:
        images = tif.asarray()  # Read the entire TIFF as a numpy array
        metadata = tif.series[0].axes  # Get axes information
        
    if 'C' not in metadata or 'Z' not in metadata:
        raise ValueError("The TIFF file doesn't have channels or z-planes")

    # Get the index of channels and z-planes
    channel_idx = metadata.index('C')
    z_plane_idx = metadata.index('Z')

    # Get the number of channels and z-planes
    num_channels = images.shape[channel_idx]
    num_z_planes = images.shape[z_plane_idx]

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Split and save each channel and z-plane
    for c in range(num_channels):
        for z in range(num_z_planes):
            # Select the appropriate channel and z-plane
            single_image = images.take(c, axis=channel_idx).take(z, axis=z_plane_idx)
            # Save the image
            output_filename = f'channel_{c+1}_z_{z+1}.tiff'
            output_path = os.path.join(output_dir, output_filename)
            tifffile.imwrite(output_path, single_image)

    print(f"Saved {num_channels * num_z_planes} images to {output_dir}")

# Usage example:
tiff_path = 'OneDrive\\Desktop\\GIS attachment\\confocal testing\\test.tif'
output_dir = 'C:\\Users\\Jeremy\\OneDrive\\Desktop\\GIS attachment\\confocal testing\\output'
split_tiff(tiff_path, output_dir)