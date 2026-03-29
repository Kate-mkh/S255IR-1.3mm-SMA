#type in casa: exec(open("Image_to_fits.py").read())

import glob
from casatools import image

#folder = '../data/intermediate/images/' #to run in src
folder = 'images/' #to run in data

image_files = sorted(glob.glob(f'{folder}*.image'))

ia = image()

for image_path in image_files:
    fits_path = image_path.replace('.image', '.fits')
    
    if os.path.exists(fits_path):
            print(f'Already exists: {fits_path}')
            continue    

    ia.open(image_path)
    ia.tofits(fits_path, dropdeg=True)
    ia.close()

    print(f'Saved: {fits_path}')
