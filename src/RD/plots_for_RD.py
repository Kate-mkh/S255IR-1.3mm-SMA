import numpy as np
import matplotlib.pyplot as plt

file1 = '../../data/intermediate/sma1.txt' #spectrum from CLASS with command `greg sma1.txt /formatted`
file2 = '../../data/intermediate/lines_sma1/H2CO_lines.txt'

data1 = np.loadtxt(file1, comments='#')

with open(file2, 'r') as f:
    lines = f.readlines()

header = lines[0]
processed_lines = [header]  
num_lines_to_check = 16
lines_checked = 0

for line in lines[1:]:
    if line.strip().startswith('#'):
        processed_lines.append(line)
        continue

    parts = line.strip().split('\t')
    if len(parts) < 4:
        parts += [''] * (4 - len(parts))  

    if parts[3].strip() == '' and lines_checked < num_lines_to_check:
        try:
            frequency = float(parts[0])
        except ValueError:
            processed_lines.append(line)
            continue

        mol = parts[1]

        lower_bound = frequency - 30
        upper_bound = frequency + 30
        mask = (data1[:, 0] >= lower_bound) & (data1[:, 0] <= upper_bound)
        plt.step(data1[mask, 0], data1[mask, 1], where='mid', label=f'Frequency: {frequency} MHz')

        plt.xlabel('Frequency (MHz)')
        plt.ylabel('Temperature')
        plt.title('Temperature vs Frequency')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.ylim([-0.5, 3])
        plt.text(frequency, 1.5, mol,
                 verticalalignment='bottom', horizontalalignment='right',
                 color='black', fontsize=12)
        plt.axvline(frequency, 0, 2.5)

        plt.show()

        answer = input('Is it a good line? (y/n): ').strip().lower()
        parts[3] = answer
        lines_checked += 1

    processed_lines.append('\t'.join(parts) + '\n')

with open(file2, 'w') as f:
    f.writelines(processed_lines)

print(f'\nUpdated: {file2}')
