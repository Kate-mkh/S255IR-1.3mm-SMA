import os
import shutil
import glob
import subprocess
import zipfile

def rename_file(filename):
    name = filename.replace('.pdf', '').replace('.fits', '')
    if '+' in name:
        name = name.replace('+', 'plus')
    parts = name.split('_')
    for i, part in enumerate(parts):
        if '.' in part:
            parts[i] = part.replace('.', '_')
    return '_'.join(parts) + ('.pdf' if filename.endswith('.pdf') else '.fits')

def copy_and_rename_files(src_dir, dest_dir, extension):
    os.makedirs(dest_dir, exist_ok=True)
    files = glob.glob(os.path.join(src_dir, f'*{extension}'))
    
    for file_path in files:
        new_name = rename_file(os.path.basename(file_path))
        dest_path = os.path.join(dest_dir, new_name)
        shutil.copy2(file_path, dest_path)
        print(f"Copied {os.path.basename(file_path)} to {new_name}")

def create_individual_fits_zips(fits_dest):
    individual_zips_dir = os.path.join(fits_dest, "individual_zips")
    os.makedirs(individual_zips_dir, exist_ok=True)
    
    fits_files = glob.glob(os.path.join(fits_dest, "*.fits"))
    
    for fits_file in fits_files:
        filename = os.path.basename(fits_file)
        zip_name = filename.replace('.fits', '.zip')
        zip_path = os.path.join(individual_zips_dir, zip_name)
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(fits_file, filename)
        
        print(f"Created individual zip: {zip_name}")
    
    return individual_zips_dir

script_dir = os.path.dirname(os.path.abspath(__file__))

pdf_src = "../outputs/integrated_maps"
pdf_dest = "../outputs/web/s255ir/maps_of_integrated_intensities"
copy_and_rename_files(pdf_src, pdf_dest, ".pdf")

subprocess.run([os.path.join(script_dir, "generate_thumbs.sh")])

pdf_zip_path = os.path.join(pdf_dest, "maps_of_integrated_intensities.zip")
with zipfile.ZipFile(pdf_zip_path, 'w') as zipf:
    for file in glob.glob(os.path.join(pdf_dest, "*.pdf")):
        zipf.write(file, os.path.basename(file))
print(f"Created PDF zip archive: {pdf_zip_path}")

fits_src = "../data/intermediate/images"
fits_dest = "../outputs/web/s255ir/channel_maps"
copy_and_rename_files(fits_src, fits_dest, ".fits")

fits_zip_path = os.path.join(fits_dest, "channel_maps.zip")
with zipfile.ZipFile(fits_zip_path, 'w') as zipf:
    for file in glob.glob(os.path.join(fits_dest, "*.fits")):
        zipf.write(file, os.path.basename(file))
print(f"Created FITS zip archive: {fits_zip_path}")

individual_zips_dir = create_individual_fits_zips(fits_dest)
print(f"Individual FITS zips created in: {individual_zips_dir}")

print("\nRemember to update the config.py and run update_header_RESTFRQ.py for correct velocity display.")