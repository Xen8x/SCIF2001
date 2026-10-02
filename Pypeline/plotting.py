import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from astropy.io import fits
from helper import Filenames

df = pd.read_csv(Filenames.PHEONIX_STREAM)

x = df['ra']
y = df['dec']


scatter = plt.scatter(x, y, c = df['feh50'],marker='.', cmap='hot',s=50)
plt.xlabel('Right Ascension')
plt.ylabel('Declination')
plt.title('velocity vs metal')
cbar = plt.colorbar(scatter)
cbar.set_label('[Fe/H]')

plt.savefig('Output/phoenix_stream_Asc_vs_Dec.png', dpi=300)

plt.show()