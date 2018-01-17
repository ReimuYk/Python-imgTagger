from PIL import Image

def getAlpha(filename):
    pic = Image.open(filename)
    r,g,b,a = pic.split()
    return a

def setAlpha(pic, alpha):
    pic.putalpha(alpha)
    return pic

def consResize(pic, num, mode):
    w,h = pic.size
    if mode=='w':
        h = int(num*h/w)
        w = num
        pic = pic.resize((w,h))
    if mode=='h':
        w = int(num*w/h)
        h = num
        pic = pic.resize((w,h))
    return pic

def addEdge(pic,u,d,l,r):
    pw,ph = pic.size
    ow = pw + l + r
    oh = ph + u + d
    outpic = Image.new("RGB",(ow,oh))
    outpic.paste(pic,(l,u,pw+l,ph+u))
    return outpic

def cut(pic,w,h,l=0,u=0):
    pic = pic.crop((l,u,l+w,u+h))
    return pic
