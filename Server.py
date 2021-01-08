from PIL import Image
import requests
from io import BytesIO
import datetime
import matplotlib.pyplot as plt

import time
from IA import EvolucionDiferencial as ED



datetime_object = datetime.datetime.now()
print(datetime_object)

#IP de la camara
url = "http://192.168.100.54/cam-hi.jpg"

response = requests.get(url)
img = Image.open(BytesIO(response.content))
plt.imshow(img)

  
while(1==1):
    response = requests.get(url)
    img2 = Image.open(BytesIO(response.content))
    cambio=ED(img,img2)
    if (cambio):
        img=img2
        



datetime_object = datetime.datetime.now()
print(datetime_object)
