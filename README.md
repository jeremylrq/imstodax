# imstodax

The script converts .ims files with z planes to either .tiff or .dax files, with z planes splitted, for further downstream analysis. 

1. The choice of saving as .tiff or .dax can be toggled by modifying the save_as_dax parameter.
2. The channel list has to be inputted manually to indicate the colour that corresponds to the channel (under channel_list). It is also possible to modify the channels to extract only specific channels for analysis.
3. The bleach parameter assumes that every other hyb round is a bleach round. e.g. 00 - Hyb 0, 01 - Hyb 0 bleach...

# Workflow
1. The code first locates all .ims files in a directory.
2. If bleach is set True, the code generates the mapping of hyb and bleach rounds to the actual hyb round.
3. .ims files are then renamed to a format e.g. 07_005.tiff. Note that the code operates on the assumption that file names follow this format:
"785_WF_CMOS_4000ms_785_iRFP_CF40_Sona1_637_Cy5_CF40_Sona1_561_RFP_CF40_Sona1_785_iRFP_WF_Sona1_637_Cy5_WF_Sona1_561_RFP_WF_Sona1_2_F05.ims"
where 0_F00 refers to the hyb number (2) and the FOV (region 05). The code may need to be modified depending on the file format. The number of leading zeroes can be changed with the .zfill() parameter.
4. Each .tiff file is then parsed into their respective z stacks and colour channels. Each file is renamed to a format such as c1_02_005_z1.tiff which refers to channel 1 and the first z-plane. The channel is renamed to its actual name, based on channel_list.
5. .tiff files are converted to .dax if set to true.
6. The files are sorted to their respective z-stacks. If remove_z_label is set True, the trailing _z1 parameter will be removed.






