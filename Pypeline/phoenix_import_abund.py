import numpy as np
from astropy.io import ascii

## Read the data into pd 
table = ascii.read('Data_raw/data_abund.txt', format='cds')
df = table.to_pandas()

## Phoenix stars with only Na, O, Mg, Al
df = df[df['Star'].str.startswith('Phoenix')]
df = df[df['Species'].isin(['Na I', 'O I', 'Mg I', 'Al I'])]

values = df.pivot(index='Star', columns='Species', values='[X/Fe]')
errors = df.pivot(index='Star', columns='Species', values='e_[X/Fe]')

values = values[['Na I', 'O I', 'Mg I', 'Al I']]
errors = errors[['Na I', 'O I', 'Mg I', 'Al I']]

values.columns = ['[Na/Fe]', '[O/Fe]', '[Mg/Fe]', '[Al/Fe]']
errors.columns = ['e_[Na/Fe]', 'e_[O/Fe]', 'e_[Mg/Fe]', 'e_[Al/Fe]']

out = values.join(errors)
out.to_csv('phoenix_Na_O_Mg_Al.csv')

print(out)