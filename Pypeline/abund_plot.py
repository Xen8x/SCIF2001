import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read in data
df = pd.read_csv('Data_clean/phoenix_Na_O_Mg_Al.csv')

phon_na = df['[Na/Fe]']
phon_o = df['[O/Fe]']

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11, 4.8), constrained_layout=True)
length = np.ones(len(df['[O/Fe]']), dtype=bool)

## Na vs O (O has no errors because they're upper limits)
ax0.errorbar(df['[O/Fe]'], df['[Na/Fe]'], yerr=df['e_[Na/Fe]'], xerr=0.1, xuplims=length,fmt='o',color="#9e3911")
ax0.set_xlabel('[O/Fe]')
ax0.set_ylabel('[Na/Fe]')
ax0.set_title('Phoenix: Na vs O')
ax0.grid(alpha=0.25)

## Mg vs Al
ax1.errorbar(df['[Al/Fe]'], df['[Mg/Fe]'], xerr=df['e_[Al/Fe]'], yerr=df['e_[Mg/Fe]'], fmt='o')
ax1.set_xlabel('[Al/Fe]')
ax1.set_ylabel('[Mg/Fe]')
ax1.set_title('Phoenix: Mg vs Al')
ax1.grid(alpha=0.25)

plt.savefig('Output/phoenix_abundances.png', dpi=300)

plt.show()


 



