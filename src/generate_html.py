#!/usr/bin/env python3
"""
HTML Generator for S255IR Data Pages
Generates HTML pages for channel maps and integrated maps based on config.py
"""

import os
import sys
import shutil 
from pathlib import Path

try:
    from config import (
        FREQUENCY_MAPPING, 
        FITS_FILES_DIR, 
        TRANSITION_INFO,
        SPECIAL_CHAR_FORMATTING,
        PAGE_CONFIG,
        HTML_COLUMNS,
        CUSTOM_SORT_ORDER,
        HTML_FILES_TO_COPY
    )
except ImportError:
    print("Error: config.py not found or incomplete")
    print("Please create config.py with all required configuration variables")
    sys.exit(1)

    
    
def copy_html_files():

    print("\nCopying HTML files...")
    
    for src_path, dst_path in HTML_FILES_TO_COPY.items():
        try:
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dst_path)
            print(f"  Copied: {src_path.name} -> {dst_path}")
        except FileNotFoundError:
            print(f"  Source file not found: {src_path}")
        except Exception as e:
            print(f"  Error copying {src_path.name}: {e}")

def format_molecule_name(fits_filename):
    """
    Format molecule name from FITS filename for HTML display.
    Example: '34SO_215839_917.fits' -> '³⁴SO 215839.917 MHz'
    """
    base_name = fits_filename.replace('.fits', '')
    parts = base_name.split('_')
    molecule = parts[0]
    freq_parts = []
    for part in parts[1:]:
        clean_part = part.replace('.', '').replace('-', '')
        if clean_part.isdigit() or (clean_part.replace('+', '').isdigit() and '+' in part):
            freq_parts.append(part)
        else:
            molecule += '_' + part
    
    if len(freq_parts) == 3:
        frequency = f"{freq_parts[0]}{freq_parts[1]}.{freq_parts[2]}"
    elif len(freq_parts) == 2:
        frequency = f"{freq_parts[0]}.{freq_parts[1]}"
    elif len(freq_parts) == 1:
        frequency = freq_parts[0]
    else:
        frequency = ""
    
    for plain, formatted in SPECIAL_CHAR_FORMATTING.items():
        molecule = molecule.replace(plain, formatted)
    
    return f"{molecule} {frequency} MHz" if frequency else molecule

def get_transition_info(fits_filename):
    return TRANSITION_INFO.get(fits_filename, 'Transition information')

def get_sorted_files():

    if CUSTOM_SORT_ORDER is not None:
        sorted_files = [f for f in CUSTOM_SORT_ORDER if f in FREQUENCY_MAPPING]
        
        extra_files = [f for f in FREQUENCY_MAPPING.keys() if f not in sorted_files]
        if extra_files:
            print(f"Note: {len(extra_files)} files not in custom order, adding at the end")
            sorted_files.extend(sorted(extra_files))
            
        return sorted_files
    else:
        return list(FREQUENCY_MAPPING.keys())

def generate_html_page(fits_files, output_path, page_type='channel_maps', columns=HTML_COLUMNS):

    config = PAGE_CONFIG.get(page_type, PAGE_CONFIG['channel_maps'])
    
    html = f"""<!DOCTYPE html>
<HTML>
<HEAD>
<TITLE>{config['title']}</TITLE>
</HEAD>
<body bgcolor={config['bg_color']} text={config['text_color']} leftmargin=50>
<center>

<font size=7>{config['page_title']}</font>

<p>
<font size=5>
{config['description']}
</font>

<!-- Download all button -->
<p>
<A HREF="{config['download_file']}" style="text-decoration: none;">
<button style="background-color: {config['button_color']}; border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 12px;">
<font size=4><b>📥 {config['download_button_text']}</b></font>
</button>
</A>
</p>

<table border=0 cellpadding=15>
"""
    
    for i in range(0, len(fits_files), columns):
        html += "<tr>\n"
        
        for j in range(columns):
            idx = i + j
            if idx < len(fits_files):
                fits_file = fits_files[idx]
                base_name = fits_file.replace('.fits', '')
                display_name = format_molecule_name(fits_file)
                transition = get_transition_info(fits_file)
                thumb_path = f"{config['thumb_prefix']}{base_name}{config['thumb_suffix']}"
                file_path = f"{config['file_prefix']}{base_name}{config['file_extension']}"
                
                html += f"""<td align=center>
  <A HREF="{file_path}"><img width=150 src="{thumb_path}" hspace=10><br>{display_name}</A><br>
  <font size=2>{transition}</font>
</td>
"""
            else:
                html += "<td></td>\n"
        
        html += "</tr>\n\n"
    
    html += """</table>

<p><A HREF="../s255ir.html">Back to S255IR main page</A></p>

</center>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
def main():
    copy_html_files()
    fits_files = get_sorted_files()
    base_path = Path(FITS_FILES_DIR)
    base_path.mkdir(parents=True, exist_ok=True)
    
    channel_maps_path = base_path / "index.html"
    generate_html_page(
        fits_files=fits_files,
        output_path=channel_maps_path,
        page_type='channel_maps'
    )
    
    integrated_maps_path = base_path.parent / "maps_of_integrated_intensities" / "index.html"
    integrated_maps_path.parent.mkdir(parents=True, exist_ok=True)
    
    generate_html_page(
        fits_files=fits_files,
        output_path=integrated_maps_path,
        page_type='integrated_maps'
    )
    
    print(f"\n{'='*60}")
    print("Done! Generated two HTML pages:")
    print(f"1. Channel maps: {channel_maps_path}")
    print(f"2. Integrated maps: {integrated_maps_path}")
    print(f"\nConfiguration used:")
    print(f"  - Number of columns: {HTML_COLUMNS}")
    print(f"  - Files processed: {len(fits_files)}")
    print(f"  - Sort order: {'Custom' if CUSTOM_SORT_ORDER else 'FREQUENCY_MAPPING order'}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()