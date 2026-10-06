from __future__ import annotations
import numpy as np
from PIL import Image, ImageDraw

DEMO_RECORDS = [
    {"fdi":"13","presence":"Presente","finding":"Suspeita de cárie","score":0.66,"restoration":False,"endo":False,"quality":"Moderada","review":"Pendente"},
    {"fdi":"14","presence":"Presente","finding":"Área restaurada / revisar cárie","score":0.58,"restoration":True,"endo":False,"quality":"Moderada","review":"Pendente"},
    {"fdi":"25","presence":"Presente","finding":"Restauração","score":0.81,"restoration":True,"endo":False,"quality":"Alta","review":"Pendente"},
    {"fdi":"26","presence":"Presente","finding":"Suspeita de cárie profunda","score":0.47,"restoration":True,"endo":True,"quality":"Moderada","review":"Pendente"},
    {"fdi":"36","presence":"Presente","finding":"Sem achado","score":0.91,"restoration":False,"endo":False,"quality":"Alta","review":"Pendente"},
    {"fdi":"46","presence":"Presente","finding":"Sem achado","score":0.89,"restoration":False,"endo":False,"quality":"Alta","review":"Pendente"},
]

def draw_demo_overlay(image: Image.Image) -> Image.Image:
    img=image.convert("RGB").copy()
    draw=ImageDraw.Draw(img)
    w,h=img.size
    boxes=[(0.30,0.23,0.38,0.68,"13"),(0.22,0.25,0.31,0.69,"14"),(0.61,0.24,0.70,0.69,"25"),(0.70,0.24,0.80,0.71,"26")]
    for x1,y1,x2,y2,label in boxes:
        box=(int(w*x1),int(h*y1),int(w*x2),int(h*y2))
        draw.rectangle(box,outline="white",width=max(2,int(w/500)))
        draw.text((box[0]+4,box[1]+4),label,fill="white")
    return img

def demo_heatmap(image: Image.Image, center=(0.75,0.48), sigma=0.12) -> Image.Image:
    base=np.asarray(image.convert("RGB")).astype(np.float32)/255.0
    h,w,_=base.shape
    yy,xx=np.mgrid[0:h,0:w]
    cx,cy=center[0]*w,center[1]*h
    s=sigma*max(w,h)
    heat=np.exp(-((xx-cx)**2+(yy-cy)**2)/(2*s*s))
    overlay=base.copy()
    overlay[...,0]=np.clip(overlay[...,0]*(1-0.45*heat)+0.95*heat,0,1)
    overlay[...,1]=np.clip(overlay[...,1]*(1-0.25*heat),0,1)
    overlay[...,2]=np.clip(overlay[...,2]*(1-0.25*heat),0,1)
    return Image.fromarray((overlay*255).astype(np.uint8))
