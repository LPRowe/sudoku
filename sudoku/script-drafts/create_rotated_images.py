# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 19:50:22 2020

@author: Logan Rowe
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import scipy.ndimage
import pygame
from skimage.transform import resize

file='./graphics/replay_icon.png'

img=Image.open(file)
arr=np.asarray(img)
arr=resize(arr,(58,58),anti_aliasing=False)

lz='000'

for angle in range(360):
    if angle%5==0:
        r_arr=scipy.ndimage.rotate(arr,angle)
        plt.imsave('./graphics/rotation/'+lz[:-len(str(angle))]+str(angle)+'.png',r_arr)
        print(angle)


