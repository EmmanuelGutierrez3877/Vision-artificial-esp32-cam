from NCC import NCC
import matplotlib.pyplot as plt
import numpy as np
from random import randrange,random
import mysql.connector
import datetime
import os

def EvolucionDiferencial(img_o,img2_o):
    

    escalado=8
    img=img_o.resize(( int(img_o.size[0]/escalado), int(img_o.size[1]/escalado) ))    
    img2=img2_o.resize(( int(img2_o.size[0]/escalado), int(img2_o.size[1]/escalado) ))
    #imagen original de 800 x 600, del tamaño se dividio entre 8

    img_g = img.convert('LA')
    img2_g = img2.convert('LA')
    
    img_H,img_W = img_g.size;
    temp_H,temp_W = 10,10;
    
   
    xp = 0;
    yp = 0;

    
    ##Evolucion diferencial
    Generaciones = 25   #valores iniciales
    N = 120;     #Poblacion
    D = 2;      #dimension de la poblacion
    
    xl = 1; 
    xu =img_H-temp_W;
    xs = 1;
    
    yl = 1; 
    yu =img_W-temp_H;
    ys = 1;
    
    x,y = np.meshgrid(np.arange(xl,xu,xs),np.arange(yl,yu,ys))
    particulas = np.zeros((D,N));
    for i in range(0,N):  #asigna valores random a las posiciones y velocidades de las particulas
        particulas[0,i] = round(xl+(xu-xl)*random())
        particulas[1,i] = round( yl+(yu-yl)*random())
    
    #mejorPosicion = particulas[:,0] #las mejores posiciones al inicio son las primeras 
    F=1.2;
    cr=0.4;
    v=particulas;
    u=np.zeros((D,1))
    ra=0;
    r1=5;
    r2=1;
    r3=6;
    for G in range(0,Generaciones):
        
        for i in range(1,N):
            ##claculan las r diferentes entre si y en i
            r1=randrange(0, N)
            r2=randrange(0, N)
            r3=randrange(0, N)
            while (r1==i):
                r1=randrange(0, N)
            
            while (r2==r1)or(r2==i):
                r2=randrange(0, N)
            
            while (r3==r1)or(r3==r2)or(r3==i):
                r3=randrange(0, N)
            #
            
            
            v[:,i] = np.round(particulas[:,r1]+F*(particulas[:,r2]-particulas[:,r3])) #calcula nuevo vector
            while (v[0,i]>xu or v[0,i]<xl):
               v[0,i] = round(xl+(xu-xl)*random());
               
            while (v[1,i]>yu or v[1,i]<yl):
               v[1,i] = round(yl+(yu-yl)*random());
            
            
            for j in range (0,D):
                ra = random();
                if ra <= cr: #decide que caracteristica toma
                    u[j]=v[j,i];
                else:
                   u[j]=particulas[j,i];
                
                
            if NCC(img_g,img2_g,u[0],u[1],temp_H,temp_W) < NCC(img_g,img2_g,particulas[0,i],particulas[1,i],temp_H,temp_W) :#si es mejor lo remplaza
                particulas[:,i]=u
            
        #print(G)
    
    mejorParticula=particulas[:,1] #la mejor particula de esta generacion es la primera
    vmp = NCC(img_g,img2_g,mejorParticula[0],mejorParticula[1],temp_H,temp_W) #valor de la mejor particula
    
    for i in range (0,N):
        vsp = NCC(img_g,img2_g,particulas[0,i],particulas[1,i],temp_H,temp_W)#valor de la siguiente particula
        if (vsp < vmp ):  #si alguna de esta generacion es mejor que la anterior la remplaza
            mejorParticula=particulas[:,i]
            vmp=vsp
        
    xp=mejorParticula[0];
    yp=mejorParticula[1];
    zp=NCC(img_g,img2_g,mejorParticula[0],mejorParticula[1]);
    
    if (zp < .90 ):
        
        """#Prueba resize
        print("posicion: ",xp,yp)
        print(zp);
        plt.figure()
        plt.imshow(img2)
        plt.plot([xp, xp+temp_H], [yp, yp],'r-')
        plt.plot([xp, xp], [yp, yp+temp_W],'r-');
        plt.plot([xp+temp_H, xp+temp_H], [yp, yp+temp_W],'r-')
        plt.plot([xp, xp+temp_H], [yp+temp_W, yp+temp_W],'r-')
        plt.show()
        #"""
        
        xp=xp*escalado
        yp=yp*escalado
        temp_H=temp_H*escalado
        temp_W=temp_W*escalado
        #para pasar la coordenada a la imagen origunal se multiplica por 8, ya que fue la escala que le reducimos
        
        print("posicion: ",xp,yp)
        print(zp);
        print("diferencia\n")
        
        plt.figure()
        plt.imshow(img2_o)
        plt.plot([xp, xp+temp_H], [yp, yp],'r-')
        plt.plot([xp, xp], [yp, yp+temp_W],'r-');
        plt.plot([xp+temp_H, xp+temp_H], [yp, yp+temp_W],'r-')
        plt.plot([xp, xp+temp_H], [yp+temp_W, yp+temp_W],'r-')
        #plt.savefig('foo.png')
        senddb(plt,zp)
        #plt.show()
        return("Diferencia:"+str(zp))
    else:
        xp=xp*escalado
        yp=yp*escalado
        temp_H=temp_H*escalado
        temp_W=temp_W*escalado
        #para pasar la coordenada a la imagen origunal se multiplica por 8, ya que fue la escala que le redugimos
        
        print("posicion: ",xp,yp)
        print(zp);
        print("sin diferencia\n")
        return("Sin diferencia:"+str(zp))
    
def senddb(plt,zp):

    plt.savefig('foo.png',dpi=300, bbox_inches='tight')
    path=os.getcwd().replace("\\", "/")
    
    connection = mysql.connector.connect(
        host='localhost',
        database='Camara',
        user='root',
        password='')
    
    cursor = connection.cursor()
    
    hora = datetime.datetime.now()
    
    #print(insert,hora)
    #cursor.execute("insert into imagenes(id, fecha, imagen) values(Null, '%s', Null)",(hora.strftime('%Y-%m-%d %H:%M:%S')))
    #cursor.execute("insert into imagenes(id, fecha, imagen) values(Null, '"+hora.strftime('%Y-%m-%d %H:%M:%S')+"', load_file('"+"C:\\foo.png"+"'))")
    cursor.execute("insert into imagenes(id, fecha, imagen,NCC) values(Null, '"+hora.strftime('%Y-%m-%d %H:%M:%S')+"',LOAD_FILE('"+path+"/foo.png"+"'),'"+str(zp)+"')")
    connection.commit()
    cursor.close()
    connection.close()
    
    
    
    
