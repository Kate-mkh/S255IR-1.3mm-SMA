# make_casa_commands.py
import csv

data = []
for row in csv.DictReader(open('../data/intermediate/molecules.csv')):
    if (row['molecule'] and row['molecule'].strip() and
        row['frequency'] and row['frequency'].strip() and
        row['spw_file_number'] and row['spw_file_number'].strip() and
        row['channel_start'] and row['channel_start'].strip() and
        row['channel_end'] and row['channel_end'].strip()):
        data.append(row)

with open('../data/intermediate/split.txt', 'w') as f:
    for d in data:
        freq = d['frequency'].strip()#.replace('.', '_')
        f.write(f"split(vis='spw{d['spw_file_number'].strip()}/spw{d['spw_file_number'].strip()}.contsub',\n")
        f.write(f"      outputvis='splited/{d['molecule'].strip()}_{freq}.ms',\n")
        f.write(f"      spw='0:{d['channel_start'].strip()}~{d['channel_end'].strip()}',\n")
        f.write(f"      datacolumn='data')\n\n")

with open('../data/intermediate/tclean.txt', 'w') as f:
    for d in data:
        start = int(d['channel_start'].strip())
        end = int(d['channel_end'].strip())
        n = end - start + 1        
        freq = d['frequency'].strip()#.replace('.', '_')
        f.write(f"tclean(vis='splited/{d['molecule'].strip()}_{freq}.ms',\n")
        f.write(f"       imagename='images/{d['molecule'].strip()}_{freq}',\n")
        f.write(f"       specmode='cube',\n")
        f.write(f"       imsize=[120, 120],\n")
        f.write(f"       start=1,\n")
        f.write(f"       nchan={n-2},\n")
        f.write(f"       cell=0.5,\n")
        f.write(f"       interactive=True,\n")
        f.write(f"       niter=5000)\n\n")

with open('../data/intermediate/channels.txt', 'w') as f:
    for d in data:
        start = int(d['channel_start'].strip())
        end = int(d['channel_end'].strip())
        n = end - start + 1
        f.write(f"{d['molecule'].strip()} {d['frequency'].strip()}: {start}~{end} = {n}\n")