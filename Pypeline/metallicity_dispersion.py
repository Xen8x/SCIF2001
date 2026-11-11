import numpy as np
import pandas as pd
from helper import Filenames

## Read in both streams
data = pd.read_csv("Data_clean/c19_pristine_all_unique (3).csv")
df = pd.read_csv("Data_clean/phoenix_stream_clean2.csv")

## Metallicity and errors (drop stars with no [Fe/H])
data = data.dropna(subset=['[Fe/H]', 'e_[Fe/H]'])
df = df.dropna(subset=['feh50', 'feh_calib_std'])

c19_feh = data['[Fe/H]'].values
c19_err = data['e_[Fe/H]'].values

ph_feh = df['feh50'].values
ph_err = df['feh_calib_std'].values


## observed spread^2 = real spread^2 + error^2
## so real spread = sqrt(observed spread^2 - error^2)
def real_spread(feh, err):
    observed = np.std(feh)
    error = np.sqrt(np.mean(err**2))
    diff = observed**2 - error**2  

    return np.sqrt(diff)


for name, feh, err in [('C-19', c19_feh, c19_err), ('Phoenix', ph_feh, ph_err)]:
    print(f"{name}:  N = {len(feh)}")
    print(f"  observed spread = {np.std(feh):.5f} dex")
    print(f"  typical error   = {np.sqrt(np.mean(err**2)):.5f} dex")
    print(f"  real spread     = {real_spread(feh, err):.5f} dex")