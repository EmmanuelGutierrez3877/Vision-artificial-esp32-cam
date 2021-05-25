from PIL import Image
import requests
from io import BytesIO
import datetime
import matplotlib.pyplot as plt

import time
import numpy as np
import socket
from SendImages import SendImage,ReciveImage
from IA import senddb


mi_socket = socket.socket()
mi_socket.bind(('localhost',8000))

print("Ingrese numero de subprocesos: ")
ns=int(input())

mi_socket.listen(ns+100)
print("Server starter...")

conexiones = []
direcciones = []


#conexion con camara
datetime_object = datetime.datetime.now()
print(datetime_object)

#IP de la camara
url = "http://192.168.100.54/cam-hi.jpg"

response = requests.get(url)
img = Image.open(BytesIO(response.content))
plt.imshow(img)
senddb(plt,0)
#img=np.asarray(img).tostring()


#espera a que se conecten los procesos
while len(direcciones) < ns:
    conexion, addr=mi_socket.accept()
    conexiones.append(conexion)
    direcciones.append(addr)
    print ("conexion:",addr)
    conexion.send("Conexion establecida!".encode("ascii"))
    
    SendImage(conexion,img)
    

f =True
while True:
    #envia la actividad a cada proceso
    for conexion in conexiones:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        
        SendImage(conexion,img)
        if f:
            time.sleep((1/ns))
            print("espera...")
    f=False
        
    #espera las respuestas de cada proceso
    r=0
    while r<len(direcciones):
        for conexion in conexiones:
            resp = conexion.recv(1024).decode("ascii")
            if(len(resp)>0):
                print(resp)
                r+=1

    
conexion.close()