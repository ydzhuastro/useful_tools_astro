#!/usr/bin/env python
# coding=utf-8
# picking scatters from a plot - test
# Yongda Zhu [yzhu144@ucr.edu]
# ref: https://matplotlib.org/users/event_handling.html

import numpy as np
import matplotlib.pyplot as plt

# some random data points
continua_wave = np.random.rand(10, 100)
continua_flux = np.random.rand(10, 100)
# the selected data
diy_pick_x = np.zeros(0)
diy_pick_y = np.zeros(0)

# picking function
def onpick(event):
    global diy_pick_x,  diy_pick_y
    ind = event.ind
    print("onpick scatter:", ind, np.take(continua_wave, ind), np.take(continua_flux, ind))
    diy_pick_x = np.append(diy_pick_x, np.take(continua_wave, ind))
    diy_pick_y = np.append(diy_pick_y, np.take(continua_flux, ind))

# plot
fig, ax = plt.subplots()
col = ax.scatter(continua_wave, continua_flux, 0.3, picker=True)
fig.canvas.mpl_connect('pick_event', onpick)

plt.xlabel('Wavelength '+r'[${\rm \AA}$]')
plt.ylabel('Flux '+r'[${\rm 10^{-17} erg  s^{-1}  \AA^{-1}}$]')
plt.legend()
plt.show()
plt.close()

# print results
print "xpoints: ", diy_pick_x
print "ypoints: ",diy_pick_y

