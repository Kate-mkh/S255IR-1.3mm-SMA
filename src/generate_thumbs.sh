#!/bin/bash
# generate_thumbs.sh

if ! command -v convert &> /dev/null; then
    echo "Error: ImageMagick (convert) is not installed"
    exit 1
fi

source_dir="../outputs/web/s255ir/maps_of_integrated_intensities"
thumb_dir="$source_dir/thumbs"
mkdir -p "$thumb_dir"

for pdf_file in "$source_dir"/*.pdf; do
    if [ -f "$pdf_file" ]; then
        base_name=$(basename "$pdf_file" .pdf)
        thumb_name="$thumb_dir/${base_name}_thumb.jpg"
        
        echo "Processing: $base_name.pdf"
        
        convert -density 150 "$pdf_file[0]" -flatten -colorspace sRGB \
                -quality 85 -resize "200x200>" "$thumb_name"
        
        if [ $? -eq 0 ]; then
            echo " Created: $(basename "$thumb_name")"
        else
            echo " Failed: $base_name.pdf"
        fi
    fi
done

echo "Thumbnail generation completed!"
