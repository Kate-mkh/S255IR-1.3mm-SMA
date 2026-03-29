import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import matplotlib as mpl
import matplotlib.patches as patches
from astropy import units as u
import pyexcel_ods
import os
import warnings
import sys


from my_functions import get_ra, get_dec, find_lines, find_all_lines, plot_map

warnings.filterwarnings("ignore")

folder_path = '../data/intermediate/images/'
path_save = '../outputs/integrated/'

fits_files = [f for f in os.listdir(folder_path) if f.endswith('.fits')]

for filename in fits_files:
    fits_file = os.path.join(folder_path, filename)
    
    print(f"Processing: {filename}")
    
    data = fits.getdata(fits_file)
    header = fits.getheader(fits_file)
    beam_data = fits.getdata(fits_file, ext=1)
    beam_header = fits.getheader(fits_file, ext=1)
    
    integrated = [data[0]]
    channels = len(data)
    for i in range(1, channels):
        integrated[0] += data[i]    
    
    new_header = header.copy()
    bmaj_value = beam_data['BMAJ'][0]  
    bmin_value = beam_data['BMIN'][0]   
    bpa_value = beam_data['BPA'][0]       
    new_header.set('BMAJ', bmaj_value, 'Beam major axis FWHM [arcsec]')
    new_header.set('BMIN', bmin_value, 'Beam minor axis FWHM [arcsec]')  
    new_header.set('BPA', bpa_value, 'Beam Position Angle [degrees]')
        
    beam_data_new = beam_data[0:1].copy()
    beam_data_new['CHAN'][0] = 0
        
    hdu_beams = fits.BinTableHDU(data=beam_data_new, header=beam_header, name='BEAMS')
    
    hdu_beams.header.set('NCHAN', 1, 'Number of channels')
    
    new_fits_file_name = path_save + 'integrated_' + filename
    
    
    os.makedirs(path_save , exist_ok=True) 
    
    hdul = fits.HDUList([fits.PrimaryHDU(data=integrated, header=new_header), hdu_beams])   

    hdul.writeto(new_fits_file_name, overwrite=True)
    print("integrated file:",new_fits_file_name)        




