# Plot of SMA1 spectra
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'serif'

filename = '../data/intermediate/sma1.txt'
#filename = '../data/intermediate/sma2.gre'

data = np.loadtxt(filename)

frequencies = data[:, 0] 
brightness_temp = data[:, 1]

high_temp_indices = np.where(brightness_temp > 8)[0]
high_temp_frequencies = frequencies[high_temp_indices]


plt.figure(figsize=(10, 6))
plt.plot(frequencies, brightness_temp, linestyle='-', color='black')#marker='o',
plt.xlabel('Frequency, MHz')
plt.ylabel('T$_R$, K')
plt.title('SMA1')
#plt.title('SMA2')
plt.tick_params(direction='in', which='both', right=True, top=True) 
plt.minorticks_on()  

#sma1
labels = ['H$_2$CO', 'SO', '$^{13}$CO', 'H$_2$CO', 'CO', 'CS']
frequencies_with_labels = [211211.455, 219949.433, 220398.684, 225697.781, 230538.000, 244935.556] 
y_labels = [10, 8, 23, 10, 36, 14]

##sma2
#labels = ['H$_2$CO', '$^{13}$CO', 'H$_2$CO', 'CO', 'CS']
#frequencies_with_labels = [211211.455, 220398.684, 225697.781, 230538.000, 244935.556]  
#y_labels = [9, 20, 10.5, 29, 18]



for label, freq, y_lab in zip(labels, frequencies_with_labels, y_labels):
    plt.text(freq, y_lab, label,
             verticalalignment='bottom', horizontalalignment='right',
             color='black', fontsize=12)


y_min, y_max = max(min(brightness_temp), -2), max(brightness_temp)
y_range = y_max - y_min
plt.ylim(y_min - 0.025 * y_range, y_max + 0.1 * y_range)
#plt.grid(True)
pdf_filename = "../outputs/figures/brightness_temperature_plot_sma1_en.pdf"
plt.tight_layout()
plt.savefig(pdf_filename)
plt.show()
