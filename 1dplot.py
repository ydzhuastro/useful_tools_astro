#!/usr/bin/env python
# coding=utf-8
# plot 1-D spectra with error, written in Python3.7
# Yongda Zhu
# yzhu144@ucr.edu

import csv
import sys
import os
import re
from scipy.integrate import quad
from scipy.optimize import curve_fit
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

if (len(sys.argv) < 2):
    print('Error: argument missiong')
    print('Usuage: $ python 1dplot.py <fits name>')
    os._exit(1)

# plot a single fits
def plot_single_fits_with_error(_filename:str):
    # read fits file
    vis_sp = fits.open(_filename)
    # vis_sp.info()
    flux = vis_sp[0].data
    flux *= 10.**17
    n_pixel = flux.size
    C0 = vis_sp[0].header['CRVAL1']
    C1 = vis_sp[0].header['CDELT1']
    wave = 10.**(C0 + C1*np.arange(n_pixel))
    vis_sp.close()
    # read end

    plt.figure(figsize=(12, 6))
    plt.plot(wave, flux, linewidth=0.2, label="data", color="black")

    # read error fits
    vis_err_filename = _filename[:-5] + "e.fits"
    if os.path.exists(vis_err_filename):
        # print(vis_err_filename)
        vis_err = fits.open(vis_err_filename)
        # DEBUG vis_err.info()
        flux_err = vis_err[0].data
        flux_err *= 10.**17
        vis_err.close()
        # read err end
        plt.plot(wave, flux_err, linewidth=0.2, label="error", color="red")
    else:
        print("No error file!")

    plt.ylim(-0.5, 10)
    plt.title(_filename)
    plt.xlabel('Wavelength '+r'[${\rm \AA}$]')
    plt.ylabel('Flux '+r'[${\rm 10^{-17} erg  s^{-1}  \AA^{-1}}$]')
    plt.legend()
    plt.show()
    plt.clf()
    plt.close()
    return

# plot a single fits truncated with error
def plot_single_fits_truncated_error(_filename:str):
    # read fits file
    vis_sp = fits.open(_filename)
    # vis_sp.info()
    flux = vis_sp[0].data
    flux *= 10.**17
    n_pixel = flux.size
    C0 = vis_sp[0].header['CRVAL1']
    C1 = vis_sp[0].header['CDELT1']
    wave = 10.**(C0 + C1*np.arange(n_pixel))
    vis_sp.close()
    # read end
    # read error fits
    vis_err_filename = _filename[:-5] + "e.fits"
    if os.path.exists(vis_err_filename):
        # print(vis_err_filename)
        vis_err = fits.open(vis_err_filename)
        # DEBUG vis_err.info()
        flux_err = vis_err[0].data
        flux_err *= 10.**17
        vis_err.close()
        # read err end
    else:
        print("Error: no error file!")
        os._exit(3)

    for i in range(0, len(wave)):
        if(flux[i] < flux_err[i]):
            flux[i] = 0

    plt.figure(figsize=(12, 6))
    plt.plot(wave, flux, linewidth=0.2, label="truncated data", color="black")
    plt.plot(wave, flux_err, linewidth=0.2, label="error", color="red")
    plt.ylim(-0.5, 10)
    plt.title(_filename)
    plt.xlabel('Wavelength '+r'[${\rm \AA}$]')
    plt.ylabel('Flux '+r'[${\rm 10^{-17} erg  s^{-1}  \AA^{-1}}$]')
    plt.legend()
    plt.show()
    plt.clf()
    plt.close()
    return

# plot all fits
def plot_all_fits():
    for filename in sys.argv:
        if (filename[-5:] == '.fits') and (filename[-6:] != 'e.fits'):
            if os.path.exists(filename):
                print('plot %s' % filename)
            else:
                print('Error: file doesn\'t exist')
                os._exit(2)
            plot_single_fits_with_error(filename)

# plot all fits
def plot_all_fits_t():
    for filename in sys.argv:
        if (filename[-5:] == '.fits') and (filename[-6:] != 'e.fits'):
            if os.path.exists(filename):
                print('plot %s' % filename)
            else:
                print('Error: file doesn\'t exist')
                os._exit(2)
            plot_single_fits_truncated_error(filename)

if __name__ == "__main__":
    plot_all_fits()
