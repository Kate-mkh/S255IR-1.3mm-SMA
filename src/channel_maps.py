#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import aplpy
import matplotlib as mpl
import matplotlib.patches as patches
from astropy import units as u
import os
import warnings
import sys


from my_functions import get_ra, get_dec, plot_channel_map_whole_fits

warnings.filterwarnings("ignore") 
#You can run without warnings in terminal:
#python3 channel_maps.py config 2> /dev/null

import os

folder_path = '../data/intermediate/images/'
output_path = '../outputs/channel_maps_pdf/'

def read_input_file(input_file):
    data = []  
    colormap = None  

    with open(input_file, 'r') as f:
        for line in f:
            line = line.split('#')[0].strip()
            line = line.strip() 
            
            if not line or line.startswith('#'):  
                continue
            
            
            if line.lower().startswith("colormap"): 
                colormap = line.split('=')[1].strip()  
                continue  

            parts = line.split('\t')  
            if len(parts) == 10:  
                data.append(parts)  

    return colormap, data     



def get_filename_for_display(config_filename):

    parts = config_filename.split('_')
    if len(parts) == 3:
        #NAME_NNN_NNN.fits -> NAME_NNN.NNN.fits
        real_name = f"{parts[0]}_{parts[1]}.{'_'.join(parts[2:])}"
    elif (len(parts) > 3):
        #NAME_NAME_NNN_NNN.fits -> NAME_NAME_NNN.NNN.fits
        real_name = f"{parts[0]}_{parts[1]}_{parts[2]}.{'_'.join(parts[3:])}"
    else:
        real_name = config_filename
    
    real_name = real_name.replace('plus', '+')
    
    return real_name

def read_config():
    try:
        from config import (
            FREQUENCY_MAPPING,
            TRANSITION_INFO,
            CHANNEL_MAP_PARAMS,
            PLOT_REGION_PARAMS,
            colmap
        )
    except ImportError as e:
        print(f"Error: config.py not found or incomplete: {e}")
        print("Please create config.py with all required configuration variables")
        print("Required: FREQUENCY_MAPPING, TRANSITION_INFO")
        print("Optional: CHANNEL_MAP_PARAMS, PLOT_REGION_PARAMS, colmap")
        sys.exit(1)
    except NameError as e:
        
        try:
            from config import FREQUENCY_MAPPING, TRANSITION_INFO
        except:
            print("Error: FREQUENCY_MAPPING and TRANSITION_INFO are required in config.py")
            sys.exit(1)
            
        CHANNEL_MAP_PARAMS = {}
        PLOT_REGION_PARAMS = {}
        colmap = 'YlOrRd'
    
    default_channel_params = (0, -1, 4)  # first, last, cols
    default_region_params = (30, 110, 20, 100)
    
    data = []
    
    for config_filename, rest_freq in FREQUENCY_MAPPING.items():
        filename = get_filename_for_display(config_filename)
        fits_file = os.path.join(folder_path, filename)
        
        if not os.path.exists(fits_file):
            print(f"Warning: File {fits_file} not found, skipping...")
            continue
        
        if config_filename in CHANNEL_MAP_PARAMS:
            first_channel, last_channel, cols = CHANNEL_MAP_PARAMS[config_filename]
        else:
            first_channel, last_channel, cols = default_channel_params
        
        if config_filename in PLOT_REGION_PARAMS:
            x_0, x_end, y_0, y_end = PLOT_REGION_PARAMS[config_filename]
        else:
            x_0, x_end, y_0, y_end = default_region_params
        
        label = TRANSITION_INFO.get(config_filename, '')
        
        data.append([
            filename,
            str(first_channel),
            str(last_channel),
            str(cols),
            str(rest_freq),
            str(x_0),
            str(x_end),
            str(y_0),
            str(y_end),
            label
        ])
    
    return colmap, data

def main():

    if len(sys.argv) != 2:
        print("Usage:")
        #print("  python3 channel_maps.py input_chan_maps.txt                - for text file input")
        print("  python3 channel_maps.py config 2> /dev/null    - for config.py input")
        sys.exit(1)
    
    input_arg = sys.argv[1]
    
    if input_arg == 'config' or input_arg == 'config.py':
        print(f"Reading data from config file: {input_arg}")
        colmap, input_data = read_config()
    else:
        print(f"Reading data from text file: {input_arg}")
        colmap, input_data = read_input_file(input_arg)
    
    if not input_data:
        print("No valid data found in input source")
        sys.exit(1)
    
    os.makedirs(output_path, exist_ok=True)
    
    processed = 0
    skipped = 0
    failed = 0
    
    for parts in input_data:
        if len(parts) == 10:
            filename = parts[0]
            first_channel = int(parts[1])
            last_channel = int(parts[2])
            cols = int(parts[3])
            ref_freq = float(parts[4])
            x_0 = float(parts[5])
            x_end = float(parts[6])
            y_0 = float(parts[7])
            y_end = float(parts[8])        
            label = parts[9]
            
            fits_file = os.path.join(folder_path, filename)
            
            if not os.path.exists(fits_file):
                print(f"Warning: FITS file {fits_file} not found, skipping...")
                skipped += 1
                continue
            
            
            output_file = output_path + filename.replace(".fits", "").replace(".", "_") + ".pdf"
            output_file = output_file.replace("+", "plus")
            if os.path.exists(output_file):
                print(f"{output_file} exists.")
                skipped += 1
                continue                
            
            print(f"\nProcessing: {filename}")
            print(f"  Channels: {first_channel} - {last_channel}, cols={cols}")
            print(f"  Region: x=[{x_0}, {x_end}], y=[{y_0}, {y_end}]")
            print(f"  Label: {label}")            
            
            try:
                plot_channel_map_whole_fits(
                    fits_file, filename, output_path, ref_freq, label,
                    first_channel, last_channel, cols,
                    x_0, x_end, y_0, y_end, colmap
                )
                processed += 1
                print(f"  ✓ Successfully processed")
            except Exception as e:
                print(f"  ✗ Error processing {filename}: {e}")
                failed += 1
    
    print(f"\n{'='*50}")
    print(f"Processing complete!")
    print(f"  Successfully processed: {processed} files")
    print(f"  Skipped: {skipped} files")
    print(f"  Failed: {failed} files")
    print(f"  Total: {len(input_data)} files in input")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()