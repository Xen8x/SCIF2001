import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from astropy.coordinates import SkyCoord
from astropy import units as u
from helper import Filenames
import gala.coordinates as gc

## Read in both streams
data = pd.read_csv(Filenames.C19_STREAM)
df = pd.read_csv(Filenames.PHEONIX_STREAM)

## Distances to turn the width from degrees into pc
ph_dist = 17.5      # kpc, Shipp et al. 2018
c19_dist = 20.1     # kpc, median distance of the C-19 members


## Stream frames (same as coordinate_transform.py)
# https://iopscience.iop.org/article/10.3847/1538-4357/aacdab
icrsc__phoenix_coords = SkyCoord(ra = 311.2 * u.deg, dec = 14 * u.deg)
pole = SkyCoord(ra=icrsc__phoenix_coords.icrs.ra, dec=icrsc__phoenix_coords.icrs.dec, frame='icrs')
iscrsc_c19_coords = SkyCoord(ra = 81.45 * u.degree, dec = -6.346 * u.degree, frame = "icrs")

average_ra0 = np.mean(df['ra'])
average_ra0_c19 = np.median(data['RAICRS'])

frame = gc.GreatCircleICRSFrame.from_pole_ra0(pole=pole, ra0 = average_ra0 * u.deg)
frame2 = gc.GreatCircleICRSFrame.from_pole_ra0(pole=iscrsc_c19_coords, ra0 = average_ra0_c19 * u.deg)

PH_coords = SkyCoord(ra=df['ra'], dec=df['dec'], unit='deg', frame='icrs')
C19_coords = SkyCoord(ra=data['RAICRS'], dec=data['DEICRS'], unit='deg', frame='icrs')

ph_stream = PH_coords.transform_to(frame)
c19_stream = C19_coords.transform_to(frame2)

df['phi1'] = ph_stream.phi1.wrap_at(180 * u.degree).deg
df['phi2'] = ph_stream.phi2.deg
data['phi1'] = c19_stream.phi1.wrap_at(180 * u.degree).deg
data['phi2'] = c19_stream.phi2.deg



## Picking the stream stars


## Phoenix: the field stars have very different velocities, so keep stars within
## 50 km/s of the median, fit the velocity trend, then drop anything more than
## 3 standard deviations from the fit (repeat a few times)
ph = df[np.abs(df['vel_calib'] - np.median(df['vel_calib'])) < 50]
for i in range(5):
    fit = np.polyfit(ph['phi1'], ph['vel_calib'], 1)
    resid = ph['vel_calib'] - np.polyval(fit, ph['phi1'])
    ph = ph[np.abs(resid) < 3 * np.std(resid)]

## C-19: only the confirmed members (they have a 'note'; the stars without one aren't
## in the member list), and only the main part of the stream (within 3 deg)
c19 = data[data['note'].notna() & (np.abs(data['phi2']) < 3)]

## For velocities only use the members with spectra (GRACES / OSIRIS / UVES)
spec = c19['note'].str.contains('GRACES|OSIRIS|UVES')
c19_rv = c19[spec].dropna(subset=['Vlos'])



## Stream width: fit phi2 vs phi1, width = spread of stars around the fit

ph_track = np.polyfit(ph['phi1'], ph['phi2'], 2)
ph_width = np.std(ph['phi2'] - np.polyval(ph_track, ph['phi1']))

c19_track = np.polyfit(c19['phi1'], c19['phi2'], 1)
c19_width = np.std(c19['phi2'] - np.polyval(c19_track, c19['phi1']))



## Velocity dispersion: fit RV vs phi1, dispersion = spread of stars around the fit

ph_vfit = np.polyfit(ph['phi1'], ph['vel_calib'], 1)
ph_disp = np.std(ph['vel_calib'] - np.polyval(ph_vfit, ph['phi1']))

## C-19 velocities only cover ~9 deg and there's no real gradient, so just fit the mean (deg 0)
c19_vfit = np.polyfit(c19_rv['phi1'], c19_rv['Vlos'], 0)
c19_disp = np.std(c19_rv['Vlos'] - np.polyval(c19_vfit, c19_rv['phi1']))


print("Phoenix:  N =", len(ph))
print(f"  width = {ph_width:.3f} deg = {np.radians(ph_width) * ph_dist * 1000:.0f} pc")
print(f"  velocity dispersion = {ph_disp:.2f} km/s")
print("C-19:  N =", len(c19), " (with velocities:", len(c19_rv), ")")
print(f"  width = {c19_width:.3f} deg = {np.radians(c19_width) * c19_dist * 1000:.0f} pc  (d = {c19_dist:.1f} kpc)")
print(f"  velocity dispersion = {c19_disp:.2f} km/s")



## Plotting shennigans

c19_color = '#2a78d6'
ph_color = '#eb6834'

fig = plt.figure(figsize=(11, 7), constrained_layout=True)
ax0 = fig.add_subplot(221)
ax1 = fig.add_subplot(222)
ax2 = fig.add_subplot(223)
ax3 = fig.add_subplot(224)

x = np.linspace(ph['phi1'].min(), ph['phi1'].max(), 200)
ax0.scatter(ph['phi1'], ph['phi2'], s=20, color=ph_color)
ax0.plot(x, np.polyval(ph_track, x), 'k--')
ax0.set_ylabel(r'$\phi_2$ [deg]')
ax0.set_title(f'Phoenix width = {ph_width:.2f} deg')
ax0.grid(alpha=0.25)

ax1.scatter(ph['phi1'], ph['vel_calib'], s=20, color=ph_color)
ax1.plot(x, np.polyval(ph_vfit, x), 'k--')
ax1.set_ylabel(r'RV [km s$^{-1}$]')
ax1.set_title(f'Phoenix velocity dispersion = {ph_disp:.1f} km/s')
ax1.grid(alpha=0.25)

x = np.linspace(c19['phi1'].min(), c19['phi1'].max(), 200)
ax2.scatter(c19['phi1'], c19['phi2'], s=20, color=c19_color)
ax2.plot(x, np.polyval(c19_track, x), 'k--')
ax2.set_xlabel(r'$\phi_1$ [deg]')
ax2.set_ylabel(r'$\phi_2$ [deg]')
ax2.set_title(f'C-19 width = {c19_width:.2f} deg')
ax2.grid(alpha=0.25)

ax3.scatter(c19_rv['phi1'], c19_rv['Vlos'], s=20, color=c19_color)
ax3.plot(x, np.polyval(c19_vfit, x), 'k--')
ax3.set_xlabel(r'$\phi_1$ [deg]')
ax3.set_ylabel(r'RV [km s$^{-1}$]')
ax3.set_title(f'C-19 velocity dispersion = {c19_disp:.1f} km/s')
ax3.grid(alpha=0.25)

plt.savefig('Output/stream_width_dispersion.png', dpi=300)

plt.show()