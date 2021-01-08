from NCC import NCC
import matplotlib.pyplot as plt
import numpy as np
from random import randrange,random

def EvolucionDiferencial(img,img2):

    img=img.resize((100, 75))    
    img2=img2.resize((100, 75))

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
    for i in range (0,N):
        if (NCC(img_g,img2_g,particulas[0,i],particulas[1,i],temp_H,temp_W) < NCC(img_g,img2_g,mejorParticula[0],mejorParticula[1],temp_H,temp_W)):  #si alguna de esta generacion es mejor que la anterior la remplaza
            mejorParticula=particulas[:,i]
        
    xp=mejorParticula[0];
    yp=mejorParticula[1];
    zp=NCC(img_g,img2_g,mejorParticula[0],mejorParticula[1]);
    
    if (zp < .90 ):
        print("posicion: ",xp,yp)
        print(zp);
        print("diferencia\n")
        
        plt.figure()
        plt.imshow(img2)
        plt.plot([xp, xp+temp_H], [yp, yp],'r-')
        plt.plot([xp, xp], [yp, yp+temp_W],'r-');
        plt.plot([xp+temp_H, xp+temp_H], [yp, yp+temp_W],'r-')
        plt.plot([xp, xp+temp_H], [yp+temp_W, yp+temp_W],'r-')
        #plt.savefig('foo.png')
        plt.show()
        return('true')
    else:
        print("posicion: ",xp,yp)
        print(zp);
        print("sin diferencia\n")
        return('false')
