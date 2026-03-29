import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import aplpy
import matplotlib as mpl
import matplotlib.patches as patches
import matplotlib.ticker as ticker
mpl.use('Agg')
from astropy import units as u
import os
import warnings


def get_ra(hours, minutes, seconds):
    return (hours + ((minutes + (seconds / 60)) / 60))/24*360
def get_dec(degrees, minutes, seconds):
    return degrees+((minutes+(seconds/60))/60)

def plot_channel_map_whole_fits(fits_file, filename, path_save, ref_freq, label, first_chan, last_chan, cols, x_0, x_end, y_0, y_end, colmap):
    
    
    warnings.filterwarnings("ignore", category=UserWarning, module="aplpy")
    warnings.filterwarnings("ignore", category=UserWarning, module="astropy.wcs.wcs")
    
    
    data = fits.getdata(fits_file)
    header = fits.getheader(fits_file)
    beam_data = fits.getdata(fits_file, ext=1)
    BMAJ = beam_data['BMAJ'][0]  
    BMIN = beam_data['BMIN'][0]   
    BPA = beam_data['BPA'][0]    
    
    num_of_chans = len(data)
    if (last_chan == -1):
        num_of_chans_for_plot = abs(num_of_chans - 1 - first_chan) + 1
    else:
        num_of_chans_for_plot = abs(last_chan - first_chan) + 1
    
    
    rows = (num_of_chans_for_plot + cols - 1) // cols    
    if last_chan == -1:
        last_chan = num_of_chans - 1
    step = 1
    if first_chan > last_chan:
        step = -1
    channels = range(first_chan, last_chan + (1 * step), step)

    warnings.filterwarnings("ignore")   
    

    
    beam = True #True - if you need the beam, False - if you don't
    
    
    cmap = colmap
    cmap_coef = 1
    if cmap == 'Greys': cmap_coef = 1.1

    
    
    cmapmin = -0.2 #minimum value of colormap
    contours_percent = [ 0.5, 0.75] #percentage of the max value for contours
    shift_x = 1.5 # number in absolute value
    shift_y = 1.2 # number in absolute value
    size_x = 2 #size of the cells
    size_y = 2 #size of the cells
    gap = 0.01 #the gap between the cells
    
    
    # Calculations
    c = 299792 #speed of light
    figsize_x = cols*size_x + shift_x + 0.25 + 1.4 
    figsize_y = rows*size_y + shift_y + 0.8 
    cell_size_x = size_x / figsize_x 
    cell_size_y = size_y / figsize_y 
    gap_x = cell_size_x * gap
    gap_y = cell_size_y * gap
    shift_x_norm = shift_x / figsize_x 
    shift_y_norm = shift_y / figsize_y 
    
    
    n_channels, n_y, n_x = data.shape
    channel_width = header['CDELT3']  
    channel_start = header['CRVAL3']  
    frequencies = [channel_start + (ch * channel_width) for ch in range(n_channels)]
    
    fig = plt.figure(figsize=(figsize_x, figsize_y))
    
    if first_chan > last_chan:
        subset = data[last_chan:first_chan + 1].flatten()
    else:
        subset = data[first_chan:last_chan + 1].flatten()
    
    subset = subset[~np.isnan(subset)]       
    max_value = np.max(subset)
   
    levels = max_value * np.array(contours_percent)    
    
    for i, channel in enumerate(channels, start=0):  
        row = i // cols  
        col = i % cols   
        freq = frequencies[channel] 
        x_coord = (cell_size_x + gap_x) * col  + shift_x_norm 
        y_coord = (cell_size_y + gap_y) * (rows - 1 - row) + shift_y_norm # y-coordinate of cell bottom edge
        x_coord_cbar = (cell_size_x + gap_x) * (col + 1) + shift_x_norm # x-coordinate of colorbar left edge
        
                      
        if i != len(channels)-1 :
            warnings.filterwarnings("ignore")
            ax = aplpy.FITSFigure(fits_file, slices=[channel], figure=fig, subplot=[x_coord, y_coord, cell_size_x, cell_size_y])
            warnings.filterwarnings("ignore")
            
        if i == len(channels)-1 :
            warnings.filterwarnings("ignore")
            ax = aplpy.FITSFigure(fits_file, slices=[channel], figure=fig, subplot=[x_coord, y_coord, cell_size_x + 0.25/figsize_x , cell_size_y])
            warnings.filterwarnings("ignore")
        if i == 0: 
            molecule_freq = filename.replace(".fits", "").replace("_", " ") + ' MHz'
            ax.add_label(1.5, 1.2, molecule_freq.replace(" blend ", " ") + ' ' + label.replace("<br>", " "), relative=True, color='black', size='large')
                     
        
        ax.ax.set_xlim(x_0, x_end)
        ax.ax.set_ylim(y_0, y_end)        
         
    
        
        ax.show_contour(data[channel], levels=levels, colors='black', linewidths=0.5, zorder=1)#  cmap = 'Greys_r' 
        
        ax.show_colorscale(vmin = cmapmin, vmax = max_value * cmap_coef, cmap=cmap)      
    
        veloсity = (ref_freq - freq/1e6) * c / ref_freq
        ax.add_label(0.3, 0.9, f'{veloсity:.2f} km s$^{{-1}}$', relative=True, color='black', size='large') 
        ax.ticks.set_tick_direction('in')
        ax.ticks.set_minor_frequency(2)
        ax.tick_labels.set_xformat('hh:mm:ss')
        
        if (col > 0):
            ax.tick_labels.hide_y()
            ax.axis_labels.hide_y()
        if (row < rows - 1):
            ax.tick_labels.hide_x()
            ax.axis_labels.hide_x() 
        
        
        ra = [93.225, get_ra(6, 12, 53.77500), get_ra(6, 12, 53.84300)]
        dec = [17.989755555555554, get_dec(17, 59, 26.17), get_dec(17, 59, 23.6200)]        
    
        ax.show_markers(ra,dec,marker='^',c='black',s=20)
        
        if (row == rows - 1) & (col == 0) & (beam == True):
            rect_x = 2.5 + x_0
            rect_y = 3 + y_0
            rect_width = BMAJ*3       
            rect_height = BMAJ*3      
            
            rectangle = patches.Rectangle((rect_x, rect_y), rect_width, rect_height, linewidth=1, edgecolor='black', facecolor='white')
            
            ax.ax.add_patch(rectangle) 
            
            #show beam
            ax.show_ellipses(rect_x + rect_width/2, rect_y + rect_height/2, BMIN*2, BMAJ*2, BPA, coords_frame='pixel', zorder = 3, facecolor = 'black')
            
       
       
    
    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['ytick.direction'] = 'in'
    ax.add_colorbar()
    ax.colorbar.set_axis_label_text("Jy/beam")
    ax.colorbar.set_box([x_coord_cbar, y_coord, 0.2/ figsize_x ,cell_size_y])
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'    
    
  
    os.makedirs(path_save , exist_ok=True)    
    
    output_file = path_save + filename.replace(".fits", "").replace(".", "_") + ".pdf"
    output_file = output_file.replace("+", "plus")
    plt.savefig(output_file)
    