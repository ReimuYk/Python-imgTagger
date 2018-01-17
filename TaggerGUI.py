from tkinter import *
from PIL import Image, ImageTk
import imgedit as ie
import downloadData as dd

stat = ('','')

def click(event,num):
    print('click',num)

def ret(event):
    lst = dd.randomGet()
    path=['']
    for i in range(len(lst)):
        pth=r'./img/'+lst[i][1]+r'/'+lst[i][2]
        if lst[i][3]=='set':
            pth = pth+r'/'+lst[i][2]+r'_0'
        path.append(pth)
    for i in range(1,10):
        try:
            ib[i].showImg(path[i]+'.jpg')
        except:
            ib[i].showImg(path[i]+'.png') 
##    print(dd.randomGet())

def keypress(event):
    global stat
    c=event.keysym
    if stat[1]==c:
        stat=('','')
        print(stat)
        return
    if 'a'<=c and c<='z':
        if stat[0]=='' or stat[0]=='letter':
            stat=('letter',c)
        if stat[0]=='number':
            print('tag',stat[1],c)
    if '1'<=c and c<='9':
        if stat[0]=='' or stat[0]=='number':
            stat=('number',c)
        if stat[0]=='letter':
            print('tag',c,stat[1])
    print(stat)

def handlerAdaptor(fun,**kwds):
    return lambda event,fun=fun,kwds=kwds: fun(event,**kwds)

class imgBlock:
    def __init__(self,tk,x,y,n):
        self.tk = tk
        self.num = n
        self.imgpath = ''
        self.lx = x
        self.ly = y
    def showImg(self,path):
        self.imgpath = path
        load = Image.open(self.imgpath)
        w,h = load.size
        if w>h:
            load = ie.consResize(load,300,'w')
            w,h = load.size
            edge = int((w-h)/2)
            load = ie.addEdge(load,edge,edge,0,0)
        else:
            load= ie.consResize(load,300,'h')
            w,h = load.size
            edge = int((h-w)/2)
            load = ie.addEdge(load,0,0,edge,edge)
        render = ImageTk.PhotoImage(load)
        img = Label(self.tk,image = render)
        img.bind("<Button-1>",handlerAdaptor(click,num=self.num))
        img.image = render
        img.place(x=self.lx,y=self.ly)


root = Tk()
root.title("imgTagger")
root.geometry('1400x1000')
root.bind("<Return>",ret)
root.bind("<Key>",keypress)
can = Canvas(root,width=1000,height=1000)
can.place(x=0,y=0)

ib7 = imgBlock(root,20,20,7)
ib8 = imgBlock(root,350,20,8)
ib9 = imgBlock(root,680,20,9)
ib4 = imgBlock(root,20,350,4)
ib5 = imgBlock(root,350,350,5)
ib6 = imgBlock(root,680,350,6)
ib1 = imgBlock(root,20,680,1)
ib2 = imgBlock(root,350,680,2)
ib3 = imgBlock(root,680,680,3)
ib = ['',ib1,ib2,ib3,ib4,ib5,ib6,ib7,ib8,ib9]

##ib7.showImg('./img/test.png')
##ib5.showImg('./img/5.jpg')
##ib3.showImg('./img/7.jpg')


can.create_line(0,0,1000,1000)
rec = can.create_rectangle(10,10,340,340,width=5,outline='red')

Label(root,text='tag1',bg='red').place(x=200,y=200)

#root.update()
root.mainloop()

