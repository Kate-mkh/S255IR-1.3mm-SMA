from astropy.io import fits
import os
from pathlib import Path
import config

def update_fits_frequency(): #from config
    
    fits_dir = Path(config.FITS_FILES_DIR).resolve()
    
    if not fits_dir.exists():
        print(f"Error: dir {fits_dir} does not exist!")
        return
    
    success_count = 0
    error_count = 0
    
    for filename, correct_frequency in config.FREQUENCY_MAPPING.items():
        try:
            file_path = fits_dir / filename
            print(f"Processing {filename}...")
            
            if not file_path.exists():
                print(f"  No file: {file_path}")
                error_count += 1
                continue
            
            with fits.open(file_path, mode='update') as hdul:
                header = hdul[0].header
                
                if 'RESTFRQ' in header:
                    correct_frequency *= 1000000
                    old_freq = header['RESTFRQ']
                    header['RESTFRQ'] = correct_frequency
                    print(f"  RESTFRQ: {old_freq} -> {correct_frequency}")
                    success_count += 1
                else:
                    print(f" There are no RESTFRQ, sorry...")
                
                hdul.flush()
                
            print(f" Success\n")
            
        except Exception as e:
            print(f" Errors: {e}\n")
            error_count += 1
    
    print(f"Success: {success_count}")
    print(f"Errors: {error_count}")

if __name__ == "__main__":
    update_fits_frequency()