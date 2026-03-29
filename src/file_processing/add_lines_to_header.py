from astropy.io import fits

def add_lines_to_header(fits_file_path):
    new_header = {'OBJECT': 'S255IR REG2',
                  'EQUINOX': 2000.0,
                  'BUNIT': 'Jy/beam',
                  'TELESCOP': 'SMA',
                  'OBSERVER': 'syliu',
                  'DATE-OBS': '2020-10-06',
                  'UT': '14:57:22.2'}

    with fits.open(fits_file_path, mode='update') as hdul:
        header = hdul[0].header
        
        if 'RESTFRQ' in header:
                    header.remove('RESTFRQ')        
        
        for key, value in new_header.items():
            header[key] = value  
            
        hdul.flush()
    
    print('Success')	

add_lines_to_header('../data/intermediate/sma1/spw1.fits')


