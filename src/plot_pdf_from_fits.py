import os
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
import matplotlib as mpl
import matplotlib.patches as patches


def get_ra(hours, minutes, seconds):
    return (hours + ((minutes + (seconds / 60)) / 60)) / 24 * 360

def get_dec(degrees, minutes, seconds):
    return degrees + ((minutes + (seconds / 60)) / 60)

def plot_all_fits(input_dir, output_dir, x_0, x_end, y_0, y_end):
    os.makedirs(output_dir, exist_ok=True)
    
    fits_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.fits')]
    
    label = True
    colorbar_ = True
    levels_ = True
    markers = True
    beam = True
    
    contours_percent = [0.5, 0.75]  # percentage of the max value for contours
    
    for fname in fits_files:
        fpath = os.path.join(input_dir, fname)
        
        pdf_name = os.path.splitext(fname)[0] + ".pdf"
        pdf_path = os.path.join(output_dir, pdf_name)
        
        with fits.open(fpath) as hdul:
            data = hdul[0].data
            header = hdul[0].header
        
        wcs_original = WCS(header)
        wcs_2d = wcs_original.celestial
        
        if data.ndim == 3:
            plot_data = data[0, :, :]
        else:
            plot_data = data
        
        data_clean = np.nan_to_num(plot_data, nan=0.0, posinf=0.0, neginf=0.0)
        
        fig = plt.figure(figsize=(9, 9))
        ax = fig.add_subplot(111, projection=wcs_2d)
        
        im = ax.imshow(data_clean, cmap='YlOrRd', origin='lower', aspect='equal')  
        
        ax.set_xlim(x_0, x_end)
        ax.set_ylim(y_0, y_end)
        
        ax.set_aspect('equal')
        
        ra = ax.coords[0]
        dec = ax.coords[1]
        ra.set_axislabel('Right Ascension (J2000)')
        dec.set_axislabel('Declination (J2000)')
        ra.set_major_formatter('hh:mm:ss')
        dec.set_major_formatter('dd:mm:ss')
        
        ax.grid(color='white', ls='solid', alpha=0.3)
        
        if colorbar_:
            cbar = plt.colorbar(im, ax=ax, pad=0.05)
            cbar.set_label("Jy/beam")
        
        if levels_:
            max_value = np.max(data_clean)
            print(f"Max value for {fname}: {max_value}")
            levels = max_value * np.array(contours_percent)
            ax.contour(data_clean, levels=levels, colors='black', linewidths=0.5)
        
        if markers:
            ra_coords = [93.225, get_ra(6, 12, 53.77500), get_ra(6, 12, 53.84300), get_ra(6, 12, 54.03)]
            dec_coords = [17.989755555555554, get_dec(17, 59, 26.17), get_dec(17, 59, 23.6200), get_dec(17, 59, 11.5)]
            
            for ra_val, dec_val in zip(ra_coords, dec_coords):
                ax.plot(ra_val, dec_val, '^', color='black', 
                       markersize=8, markeredgecolor='black', transform=ax.get_transform('world'))
        
        if beam and 'BMAJ' in header and 'BMIN' in header and 'BPA' in header:
            BMAJ = header['BMAJ']
            BMIN = header['BMIN']
            BPA = header['BPA']
            
            rect_x = 2.5 + x_0
            rect_y = 3 + y_0
            rect_width = BMAJ * 3
            rect_height = BMAJ * 3
            
            rectangle = patches.Rectangle((rect_x, rect_y), rect_width, rect_height,
                                         linewidth=1, edgecolor='black', facecolor='white')
            ax.add_patch(rectangle)
            
            beam_x = rect_x + rect_width / 2
            beam_y = rect_y + rect_height / 2
            
            beam_width = BMIN * 2
            beam_height = BMAJ * 2
            
            beam_ellipse = patches.Ellipse((beam_x, beam_y), beam_width, beam_height,
                                          angle=BPA, 
                                          linewidth=1, 
                                          edgecolor='black', 
                                          facecolor='black',
                                          zorder=3)
            ax.add_patch(beam_ellipse)
        
        plt.savefig(pdf_path, bbox_inches='tight', dpi=300)
        plt.close(fig)
        
        print(f"Saved: {pdf_path}")
    
    print("Done")

plot_all_fits(
    input_dir="../outputs/integrated",
    output_dir="../outputs/integrated_maps", 
    x_0=20, x_end=100, y_0=20, y_end=100
)