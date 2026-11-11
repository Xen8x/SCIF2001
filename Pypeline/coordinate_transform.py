import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy import units as u
from helper import Filenames
import gala.coordinates as gc 

filepath = 'DATA_raw/s5_pdr1.fits'

def get_data():
    data = fits.getdata(filepath)
    df = pd.DataFrame(data)

    df = df[df['field'].str.contains("phoenix", case=0)]
 
    df = df[df['primary'] == 1]

    #df = df[(df["priority"] == 4 )| (df["priority"] == 5)]
    df = df[(df["priority"] == 9)]
    return df



data = pd.read_csv(Filenames.C19_STREAM)
# ra=data['ra']
# dec=data['dec']

df = get_data()
# https://iopscience.iop.org/article/10.3847/1538-4357/aacdab
icrsc__phoenix_coords = SkyCoord(ra = 311.2 * u.deg, dec = 14 * u.deg)
pole = SkyCoord(ra=icrsc__phoenix_coords.icrs.ra, dec=icrsc__phoenix_coords.icrs.dec, frame='icrs')
iscrsc_c19_coords = SkyCoord(ra = 81.45 * u.degree, dec = -6.346 * u.degree, frame = "icrs")

average_ra0_c19 = np.median(data['RAICRS'])

average_ra0 = np.mean(df['ra'])

# 
frame = gc.GreatCircleICRSFrame.from_pole_ra0 (pole=pole,ra0 = average_ra0 * u.deg)
frame2 = gc.GreatCircleICRSFrame.from_pole_ra0(pole=iscrsc_c19_coords,ra0 = average_ra0_c19 * u.deg)

PH_coords = SkyCoord(ra=df['ra'], dec=df['dec'], unit='deg', frame='icrs')
C19_coords = SkyCoord(ra=data['RAICRS'], dec=data['DEICRS'], unit='deg', frame='icrs')

ph_stream = PH_coords.transform_to(frame)
c19_stream = C19_coords.transform_to(frame2)



x = ph_stream.phi1.wrap_at(180 * u.degree).radian
y = ph_stream.phi2.radian

x2 = c19_stream.phi1.wrap_at(180 * u.degree).radian
y2 = c19_stream.phi2.radian

# x = PH_coords.galactic.l.wrap_at(180 * u.deg).radian
# y = PH_coords.galactic.b.radian

# xnorm = PH_coords.ra.wrap_at(180 * u.deg).radian
# ynorm = PH_coords.dec.radian

# x2 = C19_coords.galactic.l.wrap_at(180 * u.deg).radian
# y2 = C19_coords.galactic.b.radian

# x2norm = C19_coords.ra.wrap_at(180 * u.deg).radian
# y2norm = C19_coords.dec.radian

# print(x)
# print(y)
fig = plt.figure(figsize=(16, 8),constrained_layout=True)
ax0 = fig.add_subplot(221, projection='mollweide')
ax1 = fig.add_subplot(222, projection='mollweide')
ax2 = fig.add_subplot(223,projection='mollweide')
ax3 = fig.add_subplot(224, projection="mollweide")


cmap = 'viridis'
vmin, vmax = -4, -1

sc = ax0.scatter(PH_coords.ra.wrap_at(180*u.deg).radian, PH_coords.dec.radian,
                 s=20, c=df['feh50'], cmap=cmap, vmin=vmin, vmax=vmax)
ax0.scatter(C19_coords.ra.wrap_at(180*u.deg).radian, C19_coords.dec.radian,
            s=20, c=data['[Fe/H]'], cmap=cmap, vmin=vmin, vmax=vmax)
ax0.grid(True)
ax0.set_title("ICRS Frame")
ax1.scatter(PH_coords.galactic.l.wrap_at(180*u.deg).radian, PH_coords.galactic.b.radian,
            s=20, c=df['feh50'], cmap=cmap, vmin=vmin, vmax=vmax)
ax1.grid(True)
ax1.scatter(C19_coords.galactic.l.wrap_at(180*u.deg).radian, C19_coords.galactic.b.radian,
            s=20, c=data['[Fe/H]'], cmap=cmap, vmin=vmin, vmax=vmax)
ax1.set_title("Galactic Frame")
ax2.scatter(x, y, s=40, c=df['feh50'], cmap=cmap, vmin=vmin, vmax=vmax)
ax2.grid(True)
ax3.scatter(x2, y2, s=40, c=data['[Fe/H]'], cmap=cmap, vmin=vmin, vmax=vmax)
ax2.set_title("Phoenix Stream Frame")
ax3.grid(True)
fig.colorbar(sc, ax=[ax0, ax1, ax2, ax3], label='[Fe/H]')
ax3.set_title("C19 Stream Frame")

plt.show()
