import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from helper import Filenames
from astropy.io import fits

filepath = filepath = 'DATA_raw/s5_pdr1.fits'

def get_data():
    data = fits.getdata(filepath)
    df = pd.DataFrame(data)

    df = df.astype({'field': str, 'feh50': float, 'vel50': float})
    df = df[df['field'].str.contains("phoenix", case=0)]

    df = df[df['primary'] == 1]

    #df = df[(df["priority"] == 4 )| (df["priority"] == 5)]
    df = df[(df["priority"] == 9)]
    print(len(df))
    return df

## Read in both streams
data = pd.read_csv(Filenames.C19_STREAM)
df = get_data()

## Metallicity distribution for both streams
## Removing incomplete data (NaN) from dataset to remove errors
data = data.dropna(subset=['[Fe/H]', 'e_[Fe/H]'])
df = df.dropna(subset=['feh50', 'feh_calib_std'])


c19_feh = data['[Fe/H]']
c19_err = data['e_[Fe/H]']

ph_feh = df['feh50']
ph_err = df['feh_calib_std']





x = np.linspace(-4.25, 0, 500)
bins = np.arange(-4.25, 0.25, 0.25)

c19_color = '#2a78d6'
ph_color = '#eb6834'

## Plotting the metallicity distribution
plt.figure(figsize=(7, 4.8))

## C-19 Stream Metallicity fits 
plt.hist(c19_feh, bins=bins, density=True, histtype='stepfilled', color=c19_color, alpha=0.18)
plt.hist(c19_feh, bins=bins, density=True, histtype='step', color=c19_color, linewidth=1.5)
plt.axvline(np.median(c19_feh), color=c19_color, linestyle='--', linewidth=1)


## Phoenix Stream metallicty fits
plt.hist(ph_feh, bins=bins, density=True, histtype='stepfilled', color=ph_color, alpha=0.18)
plt.hist(ph_feh, bins=bins, density=True, histtype='step', color=ph_color, linewidth=1.5)
plt.axvline(np.median(ph_feh), color=ph_color, linestyle='--', linewidth=1)

print("Phoenix median [Fe/H]:", np.median(ph_feh))
print("C-19 median [Fe/H]:", np.median(c19_feh))

plt.xlim(-4.25, 0)
plt.xlabel('[Fe/H]')
plt.ylabel('Normalised density')
plt.title(f'Metallicity distribution ([Fe/H] = )')
plt.legend(frameon=False)
plt.grid(alpha=0.25)

plt.savefig('Output/metallicity_distribution.png', dpi=300)

plt.show()