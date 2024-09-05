# Introduction

The script converts .ims files with z planes to either .tiff or .dax files, with z planes splitted, for further downstream analysis. 

.ims files are a proprietary image format of Andor confocal microscopes from Oxford Instruments. Unfortunately the .ims files are not very amenable to robust analysis by common imaging pipelines which usually rely on other file formats. Our lab performs MERFISH (multiplexed error-robust FISH), a genetic technique, and we are newly interested in z-plane analysis of regions of cells to study spatial gene distribution by microscopy. Currently, the lab does not have a pipeline to analyse individual z-planes and we rely on a maximum intensity projection of the entire z-stack which may not be spatially accurate. The script accomplishes this through these steps:

1. Conversion of .ims to .tiff files
2. Bleach hybridisation map
3. Renaming of .tiff files
4. Parsing .tiff files into individual channels and z stacks
5. Conversion of .tiff to .dax files
6. Sorting of .tiff / .dax files into respective z-planes
   
# Code overview
`channel_list`: to be inputted manually. Maps the channel in the .ims image to the channel eventually appended to the front of the file. e.g. Channel 1 - Cy3... Note that it is also possible for a subset of channels to be selected, e.g. c4-c6. However, this also requires modifying code under `process_tiff`.

`save_as_dax`: to toggle between saving as a .dax or .tiff file. .dax files are originally built for STORM microscope analysis under the Zhuang lab in Harvard. Some multiplexed FISH pipelines rely on the .dax image format. Nevertheless, setting it as False will save images in the more common .tiff format.

`remove_z_label`: usually set to True, as it makes the file format neater. The z-label is used to sort images into their respective z-plane at the end of analysis.

`bleach`: can be toggled between True and False. In a multiplexed FISH workflow we have alternate rounds of hybridisation (for our fluorescently-labelled readouts) and bleaching (to remove our fluorescently-labelled readouts). However the Imaris acquisition software simply saves each imaging round in ascending order and bleach rounds will be obscured. Set to True to include bleach labelling.

`first_hybnum` and `final_hybnum`: the hyb numbers that were originally saved during image acquisition. 

# Detailed workflow

# 1. Conversion of .ims to .tiff files
We first set the working directory for the analysis to be done via the Tk library, and retrieve all .ims files into a list via the glob library. The .ims list is then passed into the `driver` function which converts all .ims files into .tiff files but leaving the original .ims files intact. This utilises code from the Oakes lab repository, who developed the .ims to .tiff conversion. The code works because the h5py library is able to read .ims files. The code has been slightly modified to return a list of all the converted tiffs. This design choice was chosen so that existing .tiff files in the directory would not be touched for subsequent processing.

# 2. Bleach hybridisation map
This code will only run if bleach is toggled.

For a given imaging session, the images will be generated sequentially: 00, 01, 02, 03... However due to alternating hybridisation and bleaching rounds it should be set to 00, Bleach_00, 01, Bleach_01... instead. The code achieves this by generating a dictionary to map the hybridisation rounds to the actual hyb/bleach cycle. We need to consider two separate scenarios of the first hyb being either even or odd, as the numbering logic would be slightly different.

# 3. Renaming of .tiff files
.ims files are then renamed to a format e.g. 07_005.tiff. Note that the code operates on the assumption that file names follow this format:
>"785_WF_CMOS_4000ms_785_iRFP_CF40_Sona1_637_Cy5_CF40_Sona1_561_RFP_CF40_Sona1_785_iRFP_WF_Sona1_637_Cy5_WF_Sona1_561_RFP_WF_Sona1_2_F05.ims"

where 2_F05 refers to the hyb number (2) and the FOV (region 05). The code can be modified to suit the file name formatting. The number of leading zeroes can be changed with the `.zfill()` parameter. 

If bleach is toggled, we need to append 'Bleach' to every alternate hybridisation round. The code logic has to be kept separate via `evenhybs` because `hybmap` does not store the bleach rounds.

# 4. Parsing .tiff files into individual channels and z stacks
Each .tiff file is then parsed into their respective z stacks and colour channels through the `process_tiff` function. In this function, we utilise the tifffile library to read the tiff and retrieve each individual frame. Each file is renamed to a format such as c1_02_005_z1.tiff; this refers to channel 1 and the first z-plane. Note that it is possible to toggle the `num_channels` parameter in the code to extract only a specific subset of channels if desired. 

We then have another function, `rename_tiff`, to convert the channel (c1) into its proper name via the mapping given by `channel_list`. The naming has to match up for the code to work. The channel is renamed to its actual name, based on the inputs to `channel_list`. The code returns a list of renamed .tiff files.

# 5. Conversion of .tiff to .dax files
If `save_as_dax` is True, a conversion of .tiff to .dax will be performed. This utilises code from the Zhuang lab.

# 6. Sorting of .tiff / .dax files into respective z-planes
The files are sorted into their individual z-planes utilising the trailing _z label. First, we grab all files in the directory and any .tiff files are removed if we are saving only .dax files. The code first searches for a matching z-index and constructs a folder for that z-index. Then, if `remove_z_label` is set True, the trailing _z parameter will be removed through a simple renaming. Generally this is set to True to make the output neater. Finally we move the photo into the z-folder.

# tiff-dax converter

The `tiffdaxconverter.py` script can also be run independently to convert dax to tiff files and vice versa. It does the conversion for all valid files in the working directory. For the .tiff to .dax conversion, we need to first rename all .tif to .tiff files because the tifffile library only recognises the .tiff extension.

# Credits

The `tiffdaxconverter.py` file is modified from the Zhuang lab repository: https://github.com/ZhuangLab/storm-analysis/tree/71ae493cbd17ddb97938d0ae2032d97a0eaa76b2

The `imstotiff.py` file is modified from the Oakes lab repository: https://github.com/OakesLab/ims-to-tif-converter
