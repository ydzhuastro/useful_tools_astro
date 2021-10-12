import numpy as np
import cv2
from mss import mss
from PIL import Image
import os, argparse
from numpy.fft import fft2, ifft2, fftshift
import time
import pyautogui
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata

import lmfit
from lmfit.lineshapes import gaussian2d

# make sure the scale on the guider TV is 29"
# use shift+cmd+4 to measure the pixel coordinates of the star
star_x = 742
star_y = 325

# center of Keck II hand paddle
paddle_x = 334
paddle_y = 423

# auto mouse click
auto_click = False

mon = {'left': star_x-13, 'top': star_y-13, 'width': 27, 'height': 27}

x, y = np.meshgrid(np.arange(0, 54, 1), np.arange(0, 54, 1))


with mss() as sct:
    screenShot = sct.grab(mon)
    img = Image.frombytes('RGB', (screenShot.width, screenShot.height), screenShot.rgb).convert('L')
    img1 = np.array(img)
    # print(img2.shape)
    # plt.imshow(img2)
    # plt.show()
    # plt.close()

    model = lmfit.models.Gaussian2dModel()
    params = model.guess(img1.ravel(), x.ravel(), y.ravel())
    result = model.fit(img1.ravel(), x=x.ravel(), y=y.ravel(), params=params)
    lmfit.report_fit(result)

    centx0 = result.params['centerx'].value
    centy0 = result.params['centery'].value

    # cv2.imshow('test', img2)
    # plt.pcolor(x, y, img2, shading='auto')
    # plt.show()

    while True:
        time.sleep(10)
        screenShot = sct.grab(mon)
        img2 = Image.frombytes('RGB', (screenShot.width, screenShot.height), screenShot.rgb).convert('L')
        img2 = np.array(img2)
        cv2.imshow('test', img2)
        if (cv2.waitKey(500) & 0xFF) in (ord('q'), 27):
            break

        result = model.fit(img2.ravel(), x=x.ravel(), y=y.ravel(), params=params)

        centx = result.params['centerx'].value
        centy = result.params['centery'].value

        dx = np.round((centx - centx0)/4, 1)
        dy = -np.round((centy - centy0)/4, 1)
        print(dx, dy)
        if dx <= -0.5:
            print("click x+0.5")
            if auto_click:
                mx, my = pyautogui.position()
                pyautogui.moveTo(paddle_x+62, paddle_y)
                pyautogui.click(paddle_x+62,paddle_y)
                time.sleep(1)
                pyautogui.moveTo(mx, my)
        if dx >= 0.5:
            print("click x-0.5")
            if auto_click:
                mx, my = pyautogui.position()
                pyautogui.moveTo(paddle_x-62, paddle_y)
                pyautogui.click(paddle_x-62,paddle_y)
                time.sleep(1)
                pyautogui.moveTo(mx, my)
        if dy <= -0.5:
            print("click y+0.5")
            if auto_click:
                mx, my = pyautogui.position()
                pyautogui.moveTo(paddle_x, paddle_y-55)
                pyautogui.click(paddle_x,paddle_y-55)
                time.sleep(1)
                pyautogui.moveTo(mx, my)
        if dy >= 0.5:
            print("click y-0.5")
            if auto_click:
                mx, my = pyautogui.position()
                pyautogui.moveTo(paddle_x, paddle_y+55)
                pyautogui.click(paddle_x,paddle_y+55)
                time.sleep(1)
                pyautogui.moveTo(mx, my)
        # plt.imshow(img2)
        # plt.show()
        # plt.close()