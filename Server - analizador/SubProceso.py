# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 14:24:00 2021

@author: Lenovo
"""

import socket
from PIL import Image
import requests
from io import BytesIO
import datetime
import matplotlib.pyplot as plt
import time
from IA import EvolucionDiferencial as ED
from SendImages import SendImage,ReciveImage


mi_socket = socket.socket()
mi_socket.connect(('localhost',8000))

#recibe el mensaje de conexion
respuesta = mi_socket.recv(1024).decode("ascii")
print (respuesta)
img=ReciveImage(mi_socket)

#plt.imshow(img)
        


while True:
    #realiza la actividad
    img2 = ReciveImage(mi_socket)
    print("procesando")
    res=ED(img,img2)
    img=img2
    
    #envia resultados
    mi_socket.send(str(res).encode("ascii"))
    #time.sleep(0.5)


mi_socket.close()