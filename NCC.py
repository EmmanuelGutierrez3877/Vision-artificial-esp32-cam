import math

def NCC(img,img2,x,y,H=10,W=10):
    sum_img = 0.0;
    sum_img2 = 0.0;
    sum_2 = 0.0;
    
    x=int(x)
    y=int(y)

    for i in range (1,W):
        for j in range(1,H):
            sum_img = sum_img + math.pow(img.getpixel((x+j,y+i))[0],2);
            sum_img2 = sum_img2 + math.pow(img2.getpixel((x+j,y+i))[0],2);
            sum_2 = sum_2 + (img.getpixel((x+j,y+i))[0]*img2.getpixel((x+j,y+i))[0]);
    val = sum_2/(math.sqrt(sum_img)*math.sqrt(sum_img2));
    return (val)

