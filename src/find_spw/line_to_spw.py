#!/usr/bin/env python3
"""
Script to find which SPW files contain specific spectral lines.
Input: file with molecules and frequencies (MHz)
Output: mapping of lines to corresponding SPW files (cleaned and uncleaned)
"""

import os
import re
from typing import List, Tuple, Dict, Optional
from ranges import INPUT_LINES_FILE, OUTPUT_TABLE_FILE, UNCLEANED_SPW_RANGES, CLEANED_SPW_RANGES


def parse_input_file(filename: str) -> List[Tuple[str, float]]:

    lines = []
    pattern = re.compile(r'^(\S+)\s+(\d+\.\d+)\s*$')
    
    try:
        with open(filename, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                match = pattern.match(line)
                if match:
                    molecule = match.group(1)
                    frequency = float(match.group(2))
                    lines.append((molecule, frequency))
                else:
                    print(f"Warning: Line {line_num} has incorrect format: '{line}'")
    except FileNotFoundError:
        print(f"Error: Input file '{filename}' not found.")
        return []
    
    return lines

def find_spw_for_frequency(frequency: float, spw_ranges: Dict) -> List[str]:

    matching_spws = []
    
    for spw_name, (freq1, freq2) in spw_ranges.items():
        min_freq = min(freq1, freq2)
        max_freq = max(freq1, freq2)
        
        if min_freq <= frequency <= max_freq:
            matching_spws.append(spw_name)
    
    return sorted(matching_spws, key=lambda x: (int(re.search(r'\d+', x).group()) 
                                                if re.search(r'\d+', x) else 0))


def generate_output_table(lines_data: List[Tuple[str, float]]) -> List[Dict]:
    
    table = []
    
    for molecule, frequency in lines_data:
        uncleaned_spws = find_spw_for_frequency(frequency, UNCLEANED_SPW_RANGES)
        cleaned_spws = find_spw_for_frequency(frequency, CLEANED_SPW_RANGES)
        
        table.append({
            'molecule': molecule,
            'frequency': frequency,
            'uncleaned_spws': uncleaned_spws,
            'cleaned_spws': cleaned_spws,
        })
    
    return table

def write_output_file(table: List[Dict], filename: str):

    with open(filename, 'w') as f:
        
        f.write(f"{'Molecule':<15} {'Frequency(MHz)':<15} {'Uncleaned SPWs':<25} {'Cleaned SPWs':<25}\n")
        f.write(f"{'-'*15:<15} {'-'*15:<15} {'-'*25:<25} {'-'*25:<25}\n")
        
        for row in table:
            molecule = row['molecule']
            freq = f"{row['frequency']:.3f}"
            uncleaned = ', '.join(row['uncleaned_spws']) if row['uncleaned_spws'] else 'None'
            cleaned = ', '.join(row['cleaned_spws']) if row['cleaned_spws'] else 'None'
            
            f.write(f"{molecule:<15} {freq:<15} {uncleaned:<25} {cleaned:<25}\n")
        
        
        



def main():
    
    print(f"Reading input lines from '{INPUT_LINES_FILE}'...")
    lines_data = parse_input_file(INPUT_LINES_FILE)
    
    if not lines_data:
        print("No valid lines found. Exiting.")
        return
    
    print(f"Found {len(lines_data)} spectral lines.")
    
    print("Generating SPW mapping...")
    table = generate_output_table(lines_data)
    
    print(f"Writing results to '{OUTPUT_TABLE_FILE}'...")
    write_output_file(table, OUTPUT_TABLE_FILE)

if __name__ == "__main__":
    main()