import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from astropy.io import fits
from astropy.table import vstack
from astroquery.vizier import Vizier

path = "DATA_raw/C-19_memberlist_2025.csv"
write_path = "DATA_clean/c19_pristine_matched_temp.csv"
cat = "J/A+A/692/A115/pristine_dr1"

## Open CSV file with member list
df = pd.read_csv(path)
ids = df["source_id"].astype(str).tolist()

## Query Vizier with member IDs
v = Vizier(row_limit=-1, columns=["*"])
results = []
batch_size = 10

## Loop through IDs in batches
for i in range(0, len(ids), batch_size):
    batch = ids[i:i+batch_size]
    flt = "=" + ",".join(batch)      
    v.column_filters = {"GaiaDR3": flt}
    r = v.get_catalogs(cat)
    print("Processing batch:", i//batch_size + 1)

    if len(r):
        results.append(r[0])

## Stack results and export into CSV file
matched = vstack(results)
matched.write(write_path, format="ascii.csv", overwrite=True)
print(len(matched), "of", len(ids), "found")