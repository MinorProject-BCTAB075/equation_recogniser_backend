import cv2
from PIL import Image
import numpy as np

import keras

modelI=keras.models.load_model('./model/modelnew.keras')

labels_symbols = {
    10:'-', 11:'+', 12:'*', 13:'=', 14:'a', 15:'b', 16:'<', 17:'>', 18:'/',19:'√', 20:'(',21:')'
}
for i in range(0,10):
    labels_symbols[i] = chr(48+i)

symbols_folder = {'*':'times','/':'','<':'','>':'','√':'','(':'',')':''}


def get_parts_from_image(image_path):
    #image in lets say jpg format
    
    img=cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    #img=img[:int(img.shape[0]*0.995),:int(img.shape[1]*0.995)]
    
    if img is not None:
        img=~img
        ret,thresh=cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        ctrs,ret=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnt=sorted(ctrs,key=lambda ctr:cv2.boundingRect(ctr)[0])
        w=int(28)
        h=int(28)
        rects=[]
        #append to rects, the bounding boxes of all the contours
        for c in cnt:
            x,y,w,h=cv2.boundingRect(c)
            rect=[x,y,w,h]
            rects.append(rect)
            
        bool_rect=[]
        #flag all rects which represent the same symbol
        for r in rects:
            l=[]
            for rec in rects:
                #check if rec and rects overlap, i.e. are boxes for the same character flag it in bool_rect matrix
                flag=0
                if rec!=r:
                    if r[0]<(rec[0]+rec[2]+10) and rec[0]<(r[0]+r[2]+10) and r[1]<(rec[1]+rec[3]+10) and rec[1]<(r[1]+r[3]+10):
                        flag=1
                    l.append(flag)
                if rec==r:
                    l.append(0)
            bool_rect.append(l)
            
        dump_rect=[]
        #fill dump_rect with smaller of the overlapping boxes to be filtered out later
        for i in range(0,len(cnt)):
            for j in range(0,len(cnt)):
                if bool_rect[i][j]==1:
                    area1=rects[i][2]*rects[i][3]
                    area2=rects[j][2]*rects[j][3]
                    if(area1==min(area1,area2)):
                        dump_rect.append(rects[i])
                        
        final_rect=[i for i in rects if i not in dump_rect]
        
        global_bounding_box = None #a bounding box for the entire expression

        if len(final_rect)>0:
            global_bounding_box = final_rect[0]
            
        train_data=[]
        for r in final_rect:
            x=r[0]
            y=r[1]
            w=r[2]
            h=r[3]
            x2,y2 = x + r[2],y + r[3]
            if global_bounding_box[0]>x:global_bounding_box[0]=x 
            if global_bounding_box[1]>y:global_bounding_box[1]=y
            if global_bounding_box[2]<x2:global_bounding_box[2]=x2
            if global_bounding_box[3]<y2:global_bounding_box[3]=y2
            im_crop=thresh[y:y+h+10,x:x+w+10]
            im_resize=cv2.resize(im_crop,(28,28))
            train_data.append(im_resize)
        
        return train_data

def recognise_parts(imgs, symb_imgs_store=None):
    s=""
    for i in range(len(imgs)):
        if symb_imgs_store is not None:
            symb_imgs_store.append(imgs[i])
        imgs[i]=np.array(imgs[i])
        imgs[i]=imgs[i].reshape(1,28,28,1)
    #     result=modelI.predictclasses(train_data[i])
        result=np.argmax(modelI.predict(imgs[i]), axis=1)
        s+= labels_symbols[result[0]]
    return s

def predict_image(img_path):
    train_data = get_parts_from_image(img_path)
    detected_exp = recognise_parts(train_data)
    return detected_exp