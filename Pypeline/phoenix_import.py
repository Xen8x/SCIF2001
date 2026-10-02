import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from astropy.io import fits
from astropy.table import vstack
from astroquery.vizier import Vizier
from helper import Filenames
#File Path
filepath = 'DATA_raw/s5_pdr1.fits'
filepath2 = 'DATA_clean/phoenix_stream_clean2.csv'

#File to numpy shennigans 

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



def main():
    df = get_data()
    df.to_csv(filepath2, index=False)


if __name__ == "__main__":
    main()

# #To mask certain data 
# phoenix_id = df2['Stream'].astype(str).str.contains("phoenix", case=0)
# masked_data2 = df2[phoenix_id]
# masked_data3 = masked_data2["primary"] == 1
# final_data = (masked_data3["priority"] == 4) | (masked_data3["priority"] == 5)
# print(len(final_data))

# #Sorting data into arrays
# metal = masked_data['feh50']

# vel = masked_data['vel50']


#x = np.linspace(0,len(metal),len(metal))
#print(metal)


# Plotting shennigans 


Filenames.PHEONIX_STREAM    