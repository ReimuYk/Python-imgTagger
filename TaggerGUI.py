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
        self.tags = {}
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
    def addTag(self,tag):
        if tag in self.tags.keys():
            return False
        taglabel = Label(self.tk,text=tag,bg='red',width=10)
        self.tags[tag]=taglabel
        num = len(self.tags)
        px = ((num-1)%3)*107+7
        py = int((num-1)/3)
        py = 320-(py+1)*30
        taglabel.place(x=self.lx+px,y=self.ly+py)
        return True
    def removeTag(self,tag):
        if not tag in self.tags.keys():
            return False
        for k,v in self.tags.items():
            if k==tag:
                v.place_forget()
                del self.tags[tag]
                print(self.tags)
                return True
    def clearTags(self):
        for k,v in self.tags.items():
            v.place_forget()
        self.tags={}
            


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


##can.create_line(0,0,1000,1000)
rec = can.create_rectangle(10,10,340,340,width=5,outline='red')

##Label(root,text='tag1',bg='red',width=10).place(x=200,y=200)
def btclick():
    print(ib5.addTag('tagtagtag'))
    print(ib5.addTag('tag1'))
    print(ib5.addTag('tag2'))
def clear():
    ib5.clearTags()
def button3():
    ib5.removeTag('tag1')
Button(root,text='add tag',command=btclick).place(x=1100,y=200)
Button(root,text='clear tag',command=clear).place(x=1100,y=400)
Button(root,text='button3',command=button3).place(x=1100,y=600)

#root.update()
root.mainloop()

