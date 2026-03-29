import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import aplpy
import matplotlib as mpl
import matplotlib.patches as patches
from astropy import units as u
import pyexcel_ods
import os
import math
from config import FOLDER, FILES_CONFIG, PLOT_SETTINGS, SOURCES_CONFIG, VISUAL_SETTINGS, LANGUAGE_SETTINGS


def get_ra(hours, minutes, seconds):
    return (hours + ((minutes + (seconds / 60)) / 60))/24*360

def get_dec(degrees, minutes, seconds):
    return degrees+((minutes+(seconds/60))/60)

def parse_source_coordinates(sources_config):
    ra_deg_list = []
    dec_deg_list = []
    markers = []
    colors = []
    sizes = []
    labels = []
    label_coords = []
    line_params = [] 
    
    for source in sources_config:
        if 'ra_deg' in source:
            ra_deg = source['ra_deg']
        elif 'ra_hms' in source:
            h, m, s = source['ra_hms']
            ra_deg = get_ra(h, m, s)
        else:
            raise ValueError(f"Source {source['name']} has no RA coordinates")
        
        if 'dec_deg' in source:
            dec_deg = source['dec_deg']
        elif 'dec_dms' in source:
            d, m, s = source['dec_dms']
            dec_deg = get_dec(d, m, s)
        else:
            raise ValueError(f"Source {source['name']} has no DEC coordinates")
        
        ra_deg_list.append(ra_deg)
        dec_deg_list.append(dec_deg)
        markers.append(source.get('marker', '^'))
        colors.append(source.get('color', 'black'))
        sizes.append(source.get('size', 40))
        labels.append(source['name'])
        label_coords.append((source.get('label_x_pix', 0), source.get('label_y_pix', 0)))
        
        line_params.append({
            'draw_line': source.get('line', False),
            'start_x': source.get('line_start_x', 0),
            'start_y': source.get('line_start_y', 0),
            'end_x': source.get('line_end_x', 0),
            'end_y': source.get('line_end_y', 0),
            'color': source.get('line_color', 'black'),
            'width': source.get('line_width', 1),
            'style': source.get('line_style', '-')
        })
    
    return ra_deg_list, dec_deg_list, markers, colors, sizes, labels, label_coords, line_params

def setup_from_config():
    paths_fits = []
    names = []
    latex_names = []
    file_settings = []
    
    for file_config in FILES_CONFIG:
        paths_fits.append(FOLDER + file_config['filename'])
        names.append(file_config['name'])
        latex_names.append(file_config['latex_name'])
        
        settings = {}
        for key in ['beam', 'markers', 'sources', 'levels_']:
            settings[key] = file_config.get(key, PLOT_SETTINGS.get(key, True))
        file_settings.append(settings)
    
    rows = math.ceil(len(latex_names) / PLOT_SETTINGS['cols'])
    
    return paths_fits, names, latex_names, PLOT_SETTINGS, rows, file_settings

paths_fits, names, latex_names, plot_settings, rows, file_settings = setup_from_config()
ra_list, dec_list, source_markers, source_colors, source_sizes, source_labels, label_coords, line_params = parse_source_coordinates(SOURCES_CONFIG)

x_0 = plot_settings['x_0']
x_end = plot_settings['x_end'] 
y_0 = plot_settings['y_0']
y_end = plot_settings['y_end']
cols = plot_settings['cols']

cmap = VISUAL_SETTINGS['cmap']
contours_percent = VISUAL_SETTINGS['contours_percent']
shift_x = VISUAL_SETTINGS['shift_x']
shift_y = VISUAL_SETTINGS['shift_y']
size_x = VISUAL_SETTINGS['size_x']
size_y = VISUAL_SETTINGS['size_y']
gap = VISUAL_SETTINGS['gap']

frequency_unit = LANGUAGE_SETTINGS['frequency_unit']
lang = LANGUAGE_SETTINGS['language']

# Calculations
c = 299792 #speed of light
figsize_x = cols*size_x + shift_x + 0.5 * (size_x/3) + 1.4 * (cols-1) + 0.3 
figsize_y = rows*size_y + (1 + rows) * shift_y
cell_size_x = size_x / figsize_x 
cell_size_y = size_y / figsize_y 
gap_x = cell_size_x * (gap + 0.35) 
gap_y = cell_size_y * (gap + 0.2)
shift_x_norm = shift_x / figsize_x 
shift_y_norm = shift_y / figsize_y 

fig = plt.figure(figsize=(figsize_x, figsize_y))

for i, fits_file in enumerate(paths_fits, start=0):
    row = i // cols  
    col = i % cols   
    
    x_coord = (cell_size_x + gap_x) * col  + shift_x_norm
    y_coord = (cell_size_y + gap_y) * (rows - 1 - row) + shift_y_norm
    
    data = fits.getdata(fits_file)
    header = fits.getheader(fits_file)    
    
    ax = aplpy.FITSFigure(fits_file, slices=[0], figure=fig, subplot=[x_coord, y_coord, cell_size_x, cell_size_y])

    current_settings = file_settings[i]
    
    if current_settings['levels_']:
        subset = data[~np.isnan(data)]        
        max_value = np.max(subset)        
        levels = max_value * np.array(contours_percent)
        ax.show_contour(data[0], levels=levels, colors='black', linewidths=0.5, zorder=1)
    
    if (cmap == 'Greys'):
        ax.show_colorscale(cmap=cmap, vmax = max_value * 1.1)
    else:
        ax.show_colorscale(cmap=cmap, vmax = max_value)
        
    ax.ax.set_xlim(x_0, x_end)
    ax.ax.set_ylim(y_0, y_end)    

    ax.add_label(0.5, 1.14, f'{latex_names[i][0]}', relative=True, color='black', size='large')
    ax.add_label(0.5, 1.05, f'{str(latex_names[i][1])} {frequency_unit}', relative=True, color='black', size='large')  
  
    ax.ticks.set_tick_direction('in')
    ax.ticks.set_minor_frequency(1)

    if (col > 0):
        ax.axis_labels.hide_y()
    if (row < rows - 1):
        ax.axis_labels.hide_x()    
    
    if current_settings['markers']:
        for j in range(len(ra_list)):
            ax.show_markers(ra_list[j], dec_list[j], 
                          marker=source_markers[j], 
                          c=source_colors[j], 
                          s=source_sizes[j], 
                          edgecolor='white')
            
    if current_settings['sources']: #labels for markers
        for j, (label, (x_pix, y_pix)) in enumerate(zip(source_labels, label_coords)):
            if label:  
                ax.ax.text(x_pix, y_pix, label, 
                           color='black', 
                           fontsize=13,
                           ha='center',
                           va='bottom')
                
                if line_params[j]['draw_line']:
                    line = patches.ConnectionPatch(
                        (line_params[j]['start_x'], line_params[j]['start_y']),
                        (line_params[j]['end_x'], line_params[j]['end_y']),
                        coordsA='data', coordsB='data',
                        color=line_params[j]['color'],
                        linewidth=line_params[j]['width'],
                        linestyle=line_params[j]['style']
                    )
                    ax.ax.add_patch(line)
    
    if current_settings['beam']:
        BMAJ = header['BMAJ']
        BMIN = header['BMIN']
        BPA = header['BPA']
        
        rect_x = 2.5 + x_0 
        rect_y = 3 + y_0
        rect_width = BMAJ*3       
        rect_height = BMAJ*3      
        
        rectangle = patches.Rectangle((rect_x, rect_y), rect_width, rect_height, linewidth=1, edgecolor='black', facecolor='white')
        ax.ax.add_patch(rectangle)
        ax.show_ellipses(rect_x + rect_width/2, rect_y + rect_height/2, BMIN*2, BMAJ*2, BPA, coords_frame='pixel', zorder=3, facecolor='black')

    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['ytick.direction'] = 'in'
    ax.add_colorbar()
    
    if (col == cols-1):
        ax.colorbar.set_axis_label_text("Jy/beam")
    
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'      

name_for_file = cmap + '_'
for i in range(len(names)):
    name_for_file = name_for_file + names[i][0] + '_'
    

path_save = '../../outputs/map_sets/'
os.makedirs(path_save, exist_ok=True)
output_file = path_save + name_for_file + '' + lang + '.pdf'
plt.savefig(output_file)

