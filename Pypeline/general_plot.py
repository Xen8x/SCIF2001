import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy import units as u


prop_file = 'DATA_raw/sculptur_prop.fits'     
abund_file = 'DATA_raw/sculptur_abund.fits'    
name = 'Sculptor'
bin_width = 0.1                             


## Read a FITS table into pandas 
def read_fits(path):
    t = Table.read(path, hdu=1)
    t.convert_bytestring_to_unicode()
    df = t.to_pandas()
    df['Star'] = df['Star'].str.strip()
    return df

prop = read_fits(prop_file)
abund = read_fits(abund_file)

## Members 
prop = prop[prop['Sample'] == '*']

## Convert names into something nice :) from [Fe_H] to [Fe/H]
abund.columns = [c.replace('e__', 'e_[').replace('__', '[').replace('_H_', '/H]').replace('_Fe_', '/Fe]')
                 for c in abund.columns]

## Join the two tables on the star name
df = prop[['Star', 'RAJ2000', 'DEJ2000', 'RV']].merge(abund, on='Star')


## RA/Dec are converted to degrees
coords = SkyCoord(df['RAJ2000'], df['DEJ2000'], unit=(u.hourangle, u.deg), frame='icrs')
df['ra'] = coords.ra.deg
df['dec'] = coords.dec.deg

## Position relative galactic center
centre = SkyCoord(ra=np.median(df['ra']) * u.deg, dec=np.median(df['dec']) * u.deg)
offset = coords.transform_to(centre.skyoffset_frame())
df['x'] = offset.lon.to(u.arcmin).value
df['y'] = offset.lat.to(u.arcmin).value

df.drop(columns=['RAJ2000', 'DEJ2000']).to_csv(f'{name}_members.csv', index=False)

df.to_csv(f'DATA_clean/{name}_members.csv', index=False)

feh = df['[Fe/H]'].values
feh_err = df['e_[Fe/H]'].values




## Plotting shennigans
cmap = 'viridis'
color = '#2a78d6'

fig = plt.figure(figsize=(16, 4.8), constrained_layout=True)
ax0 = fig.add_subplot(131, projection='mollweide')
ax1 = fig.add_subplot(132)
ax2 = fig.add_subplot(133)

## Sky positions
## Sky positions
ra_rad = coords.ra.wrap_at(180 * u.deg).radian
dec_rad = coords.dec.radian

## Mollewide projection
sc = ax0.scatter(ra_rad, dec_rad, c=feh, s=25, cmap=cmap)
ax0.set_xlabel('RA')
ax0.set_ylabel('Dec')
ax0.set_title(f'{name}: sky')
ax0.grid(True)


sc = ax1.scatter(df['ra'], df['dec'], c=feh, s=25, cmap=cmap)                     
ax1.set_xlabel('RA [deg]')
ax1.set_ylabel('Dec [deg]')
ax1.set_title(f'{name}')
ax1.grid(alpha=0.25)
fig.colorbar(sc, ax=ax1, label='[Fe/H]')

## Metallicity histogram
bins = np.arange(np.floor(feh.min() / bin_width) * bin_width, feh.max() + bin_width, bin_width)
ax2.hist(feh, bins=bins, color=color, edgecolor='white')
ax2.set_xlabel('[Fe/H]')
ax2.set_ylabel('Number of stars')
ax2.set_title(f'{name}: metallicity ')
ax2.grid(alpha=0.25)

plt.savefig(f'Output/{name}_coords_metallicity.png', dpi=300)

plt.show()