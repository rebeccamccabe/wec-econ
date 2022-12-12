# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 15:45:40 2022

@author: rgm222
"""

import mhkit
import gridstatus
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import PySAM.Pvwattsv8 as pv

# NDBC data
ndbc_data_file = 'NDBC-46022-2021-spectrum.txt'
# downloaded from https://www.ndbc.noaa.gov/download_data.php?filename=46022w2021.txt.gz&dir=data/historical/swden/
[raw_data, meta] = mhkit.wave.io.ndbc.read_file(ndbc_data_file)
wave_data = raw_data.T
depth = 419 # m
J = mhkit.wave.resource.energy_flux(wave_data,depth) # energy flux, W/m
CW = 10 # capture width of WEC, m
P = J * CW # power of WEC, W

# plot NDBC data
fig, ax = plt.subplots()
ax.scatter(J.index, J.J)
ax.plot(J.index, np.full(np.shape(J.index),J.mean(axis=0)), c='red', label='mean')
ax.legend()
ax.set(xlabel='Time', ylabel='Energy Flux (W/m)', title='NDBC Buoy 46022 in 2021')
ax.grid()
plt.show()

# CAISO data
caiso = gridstatus.CAISO()
start = pd.Timestamp("Jan 1, 2021").normalize()
end = pd.Timestamp("Dec 31, 2021").normalize()
#lmp = caiso.get_lmp(start=start, end=end, market='REAL_TIME_HOURLY', 
#                    locations=["EUREKAA_6_N001"])
lmp = pd.read_csv('lmp-eureka-2021.csv',index_col=0)
print(lmp)

# plot CAISO data
fig, ax = plt.subplots()
ax.scatter(lmp["Time"], lmp["LMP"])
ax.set(xlabel='Time', ylabel='LMP ($/MWh)', title='CAISO Eureka Node 2021')
ax.grid()
#plt.show()

# solar data
system_model = pv.default("PVWattsNone")
#system_model.SolarResource.solar_resource_file = filename
#system_model.execute()
#print(system_model.value('annual_energy_distribution_time'))

# value of each energy source
resources = ['wave','wind','solar']
#energies = np.ones(np.shape(J.index)[0] np.size(resources))
#revenue = np.matmul(energies, lmp["LMP"])