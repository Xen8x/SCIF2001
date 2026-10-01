import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from astropy.io import fits
from astropy.table import vstack
from astroquery.vizier import Vizier


df = pd.read_csv("DATA_raw/C-19_memberlist_2025.csv")
ids = df["source_id"].astype(str).tolist()

v = Vizier(row_limit=-1, columns=["*"])
results = []
batch_size = 20
for i in range(0, len(ids), batch_size):
    batch = ids[i:i+batch_size]
    flt = "=" + ",".join(batch)      
    v.column_filters = {"GaiaDR3": flt}
    r = v.get_catalogs("J/A+A/706/A195/rgb-pgs")
    print("hello")
    if len(r):
        results.append(r[0])
    

matched = vstack(results)
matched.write("c19_pristine_matched.csv", format="ascii.csv", overwrite=True)
print(len(matched), "of", len(ids), "found")

# File Path
# filepath = 'DATA_raw/s5_pdr1.fits'
# filepath2 = 'DATA_raw/data.csv'

# File to numpy shennigans 
# link = fits.open(filepath)
# data = fits.getdata(filepath)
# df = pd.DataFrame(data)
# df2 = pd.read_csv(filepath2)

# To mask certain data 
# mask = df['field'].astype(str).str.contains("phoenix", case=0)
# masked_data = data[mask]
# phoenix_id = df2['Stream'].astype(str).str.contains("phoenix", case=0)
# masked_data2 = df2[phoenix_id]

# phoenix_id_data = masked_data['name'] 
# print(masked_data2)

# Sorting data into arrays
# metal = masked_data['feh50']

# vel = masked_data['vel50']

##x = np.linspace(0,len(metal),len(metal))
##print(metal)


## Plotting shennigans 
# plt.scatter(metal,vel,marker='.')
# plt.xlabel('metal')
# plt.ylabel('angular velocity')
# plt.title('velocity vs metal')
# plt.show()
