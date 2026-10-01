import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from astropy.io import fits


df = pd.read_csv("DATA_clean/c19_pristine_matched.csv")

metal = df['[Fe/H]']
x = np.linspace(0,len(metal),len(metal))


plt.scatter(x,metal,marker='.')
plt.xlabel('metal')
plt.ylabel('angular velocity')
plt.title('velocity vs metal')
plt.show()
