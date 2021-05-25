# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 19:55:05 2021

@author: Lenovo
"""    
import numpy as np
from PIL import Image


def SendImage(conexion,image):
    img=image
    img=np.asarray(img)
    conexion.send(img) #envia los bytes de la matriz

    
def ReciveImage(conexion):
    img=np.zeros((600,800,3))
    aux=conexion.recv(1440000)
    
    j=0
    for n in range(600):
        for b in range(800):
            for a in range(3):
                img[n][b][a] = aux[j]
                j+=1
                
    img= Image.fromarray(np.uint8(img)).convert('RGB')
    return img