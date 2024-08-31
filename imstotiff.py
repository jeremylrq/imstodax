import sys
from skimage.external.tifffile import TiffWriter
import numpy as np
import h5py
import os
from skimage.transform import pyramid_reduce
from skimage.util import img_as_float, img_as_uint
import glob
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import shutil

def get_bad_frame_index(first_time_point):
    # Now go back through the frames looking for the zeros
    # Find the index of the first zero-frame.
    # Don't know why this bug exists, but it does, so have to deal.
    # Compensate for single z-level stacks that don't need bad frame search.
    if first_time_point.shape[0] == 1:
        return 1
    first_bad_frame_index = first_time_point.shape[0] - 1
    for i_z in range(first_time_point.shape[0])[::-1]:
        if not first_time_point[i_z].any():
            first_bad_frame_index = i_z
    return first_bad_frame_index


# Return the resolution levels, time points, channes, z levels, rows, cols, etc from a ims file
# Pass in an opened f5 file
def get_h5_file_info(h5_dataset):
    # Get a list of all of the resolution options
    resolution_levels = list(h5_dataset)
    resolution_levels.sort(key = lambda x: int(x.split(' ')[-1]))

    # Get a list of the available time points
    time_points = list(h5_dataset[resolution_levels[0]])
    time_points.sort(key = lambda x: int(x.split(' ')[-1]))
    n_time_points = len(time_points)

    # Get a list of the channels
    channels = list(h5_dataset[resolution_levels[0]][time_points[0]])
    channels.sort(key = lambda x: int(x.split(' ')[-1]))
    n_channels = len(channels)
    print(n_channels)

    # Get the number of z levels
    n_z_levels = h5_dataset[resolution_levels[0]][time_points[0]][channels[0]][
                   'Data'].shape[0]
    
    z_levels = list(range(n_z_levels))

    # Get the plane dimensions
    n_rows, n_cols = h5_dataset[resolution_levels[0]][time_points[0]][channels[0]][
                    'Data'].shape[1:]


    return resolution_levels, time_points, n_time_points, channels, n_channels, n_z_levels, z_levels, n_rows, n_cols


# Convert the ims file to a tif with no downsampling performed
def convert_to_tif(f_name):
    read_file = h5py.File(f_name)
    base_data = read_file['DataSet']

    # THIS ASSUMES THAT YOU HAVE A MULTICOLOR Z STACK IN TIME
    resolution_levels, \
    time_points, n_time_points, \
    channels, n_channels, \
    n_z_levels, z_levels, \
    n_rows, n_cols = get_h5_file_info(base_data)

    # Get the index of the bad frame start
    bad_index_start = get_bad_frame_index(np.array(base_data[resolution_levels[0]][time_points[0]][channels[0]]['Data']))

    # banner_text = 'File Breakdown'
    # print(banner_text)
    # print('_'*len(banner_text))
    # print('Channels: %d' % n_channels)
    # print('Time Points: %d' % n_time_points)
    # print('Z Levels: %d' % (bad_index_start+1))
    # print('Native (rows, cols): (%d,%d)'%(n_rows, n_cols))
    # print('_'*len(banner_text))

    print(f_name.rsplit('.', maxsplit=1)[0].split('/')[-1] + '.tiff')
    with TiffWriter(f_name.rsplit('.', maxsplit=1)[0].split('/')[-1] + '.tiff', imagej=True) as out_tif:
        mmap_fname = f_name+'.mmap'
        output_stack = np.memmap(mmap_fname, dtype=np.uint16, shape=(n_time_points, bad_index_start, n_channels, n_rows, n_cols), mode='w+')

        for i_t, t in enumerate(time_points):
            print('%s/%d'%(t,n_time_points-1))
            for i_z, z_lvl in enumerate(z_levels[:bad_index_start]):
                print('%s/%d Z %d/%d'%(t, n_time_points-1, i_z+1, bad_index_start))
                for i_channel, channel in enumerate(channels):
                    output_stack[i_t, i_z, i_channel] = img_as_uint(np.array(base_data[resolution_levels[0]][time_points[i_t]][channels[i_channel]]['Data'][i_z]))

        # Save the reduced file
        out_tif.save(output_stack)

        # Delete the reduced stack
        del output_stack
        os.remove(mmap_fname)
    # changes to relocated the converted file to the image file
    new_fname = f_name.rsplit('.', maxsplit=1)[0].split('/')[-1] + '.tiff'
    current_path = os.getcwd()
    current_path = current_path.replace("\\",'/')
    path = current_path + '/'+ f_name.rsplit('.', maxsplit=1)[0].split('/')[-1] + '.tiff'
    destination ='/'.join(f_name.rsplit('.', maxsplit=1)[0].split('/')[0:])+ '.tiff' 
    shutil.move(path, destination)
    return destination



def downsample_to_tif(f_name, ds_factor=8):
    read_file = h5py.File(f_name)
    base_data = read_file['DataSet']

    # THIS ASSUMES THAT YOU HAVE A MULTICOLOR Z STACK IN TIME
    # f_name = askopenfilename(title='Choose File To Convert')
    # Hard-code the downsample factor to 8. Will make a different program for the
    # 1:1 conversion
    resolution_levels, \
    time_points, n_time_points, \
    channels, n_channels, \
    n_z_levels, z_levels, \
    n_rows, n_cols = get_h5_file_info(base_data)

    # Get the size of the downsampled image. Only going to downsample in x and y
    if ds_factor < 2:
        raise SystemExit('Downsample factor must be >=2')

    test_ds_frame = pyramid_reduce(np.array(base_data[resolution_levels[0]][time_points[0]][channels[0]]['Data'][0]), downscale=ds_factor)
    ds_n_rows, ds_n_cols = test_ds_frame.shape

    # Get the index of the bad frame start
    bad_index_start = get_bad_frame_index(np.array(base_data[resolution_levels[0]][time_points[0]][channels[0]]['Data']))

    banner_text = 'File Breakdown'
    print(banner_text)
    print('_'*len(banner_text))
    print('Channels: %d' % n_channels)
    print('Time Points: %d' % n_time_points)
    print('Z Levels: %d' % (bad_index_start+1))
    print('Native (rows, cols): (%d,%d)'%(n_rows, n_cols))
    print('Downsampled (rows, cols): (%d,%d)'%(ds_n_rows, ds_n_cols))
    print('_'*len(banner_text))

    f_ending = '_downsampled_%dX.tif' % ds_factor

    with TiffWriter(f_name.rsplit('.', maxsplit=1)[0].split('/')[-1] + f_ending, imagej=True) as out_tif:
        output_stack = np.zeros(shape=(n_time_points, bad_index_start, n_channels, ds_n_rows, ds_n_cols), dtype=np.uint16)

        for i_t, t in enumerate(time_points):
            print('%s/%d'%(t,n_time_points-1))
            for i_z, z_lvl in enumerate(z_levels[:bad_index_start]):
                print('%s/%d Z %d/%d'%(t,n_time_points-1, i_z+1, bad_index_start))
                for i_channel, channel in enumerate(channels):
                    output_stack[i_t, i_z, i_channel] = img_as_uint(
                    pyramid_reduce(img_as_float(np.array(base_data[resolution_levels[0]][time_points[i_t]][channels[i_channel]]['Data'][i_z])), downscale=ds_factor))

        out_tif.save(output_stack)
        del output_stack
    # changes to relocated the converted file to the image file
    new_fname = f_name.rsplit('.', maxsplit=1)[0].split('/')[-1] + f_ending
    current_path = os.getcwd()
    current_path = current_path.replace("\\",'/')
    path = current_path + '/'+ f_name.rsplit('.', maxsplit=1)[0].split('/')[-1] + f_ending
    destination ='/'.join(f_name.rsplit('.', maxsplit=1)[0].split('/')[0:])+ f_ending 
    shutil.move(path, destination)
    
    
def driver(passed_files, ds_factor=1):

    tiff_list = []
    # Check to make sure that the downsampling factor is a power of two
    if not bin(ds_factor).count('1') == 1:
        raise SystemExit('Invalid downsample factor. Must be a power of two.')


    if ds_factor > 1:
        downsampled = True
        converter_func = downsample_to_tif
    else:
        downsampled=False
        converter_func = convert_to_tif

    for f_name in passed_files:
        if downsampled:
            converter_func(f_name, ds_factor)
        else:
            tiff_list.append(converter_func(f_name))

    return tiff_list

