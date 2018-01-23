from tkinter import *
from PIL import Image, ImageTk
import imgedit as ie
import downloadData as dd
import data as dt

stat = ('','')

def test():
    print('test')

def click(event,num):
    print('click',num)

highlighted = []
recSize = (320,320)
recLocation = { \
    '7':(10,10), \
    '8':(340,10), \
    '9':(670,10), \
    '4':(10,340), \
    '5':(340,340), \
    '6':(670,340), \
    '1':(10,670), \
    '2':(340,670), \
    '3':(670,670)}

def highlight(numlist,color='red'):
    global highlighted
    for item in highlighted:
        can.delete(item)
    highlighted = []
    for item in numlist:
        loc = recLocation[str(item)]
        rec = can.create_rectangle(loc[0],loc[1],loc[0]+recSize[0],loc[1]+recSize[1],width=5,outline=color)
        highlighted.append(rec)

def updateData():
    # check tag comp?
    checklist = []
    for i in range(1,10):
        l = list(ib[i].tags)
        if not (('H1' in l) or ('H2' in l) or ('H3' in l) or ('H4' in l) or ('H5' in l) or ('dislike' in l)):
            checklist.append(i)
    if len(checklist)!=0:
        highlight(checklist,'#FFB90F')
        return False
    # update
    f = open('history.txt','a')
    for i in range(1,10):
        l = list(ib[i].tags)
        hmode = 0
        if 'H1' in l:hmode=1
        if 'H2' in l:hmode=2
        if 'H3' in l:hmode=3
        if 'H4' in l:hmode=4
        if 'H5' in l:hmode=5
        if hmode==0:hmode='nop'
        hmode = str(hmode)
        tags = '|'.join(l)
        dt.insert(ib[i].pid,ib[i].creator,ib[i].typ,tags,hmode)
        f.write(ib[i].pid+'\t'+ib[i].creator+'\t'+ib[i].typ+'\t'+tags+'\t'+hmode+'\n')
        dd.tag(ib[i].pid)
    dt.ci()
    dd.ci()
    return True

def ret(event):
    if not updateData():
        print('error')
        return
    randomSet()

def randomSet():
    global stat
    stat = ('','')
    for i in range(1,10):
        ib[i].clearTags()
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
        ib[i].pid = lst[i-1][2]
        ib[i].creator = lst[i-1][1]
        ib[i].typ = lst[i-1][3]

def statChange(v1,v2):
    global stat
    stat=(v1,v2)
    if stat[0]=='number':
        highlight([v2])
    else:
        highlight([])
    st.set(str(stat))

def keypress(event):
    global stat
    c=event.keysym
    if c=='Shift_L':statChange('','')
    try:
        if stat[0]=='' or stat[0]=='letter':
            can['bg']=tagKey[c][1]
        test = tagKey[c]
    except:
        if c<'1' or c>'9':return
    if stat[1]==c:
        statChange('','')
        print(stat)
        return
    avaliable = ['F1','F2','F3','F4','F5']
    if ('a'<=c and c<='z') or c in avaliable:
        if stat[0]=='' or stat[0]=='letter':
            statChange('letter',c)
        if stat[0]=='number':
            ib[int(stat[1])].tag(tagKey[c][0])
            print('tag',stat[1],c)
    if '1'<=c and c<='9':
        if stat[0]=='' or stat[0]=='number':
            statChange('number',c)
        if stat[0]=='letter':
            ib[int(c)].tag(tagKey[stat[1]][0])
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
    def tag(self,tag):
        if not self.addTag(tag):
            self.removeTag(tag)
    def addTag(self,tag):
        if tag in self.tags.keys():
            return False
        taglabel = Label(self.tk,text=tag,bg='red',width=10)
        self.tags[tag]=taglabel
        num = len(self.tags)
        px = ((num-1)%3)*107+7
        py = int((num-1)/3)
        py = 300-(py+1)*30
        taglabel.place(x=self.lx+px,y=self.ly+py)
        return True
    def removeTag(self,tag):
        if not tag in self.tags.keys():
            return False
        for k,v in self.tags.items():
            if k==tag:
                v.place_forget()
                del self.tags[tag]
                self.tagReplace()
                return True
    def tagReplace(self):
        i = 0
        for k,v in self.tags.items():
            i += 1
            px = ((i-1)%3)*107+7
            py = int((i-1)/3)
            py = 300-(py+1)*30
            v.place(x=self.lx+px,y=self.ly+py)
    def clearTags(self):
        for k,v in self.tags.items():
            v.place_forget()
        self.tags={}

tagKey={}
class tagFrame:
    def __init__(self):
        self.fm = Frame(height = 500,width = 300,relief='solid')
        self.fm.place(x=1050,y=150)
        self.addfm = Frame(self.fm,width=300)
        self.t1 = StringVar()
        Entry(self.addfm,textvariable=self.t1,width=10,relief='solid').grid(row=0,column=0)
        self.t2 = StringVar()
        Entry(self.addfm,textvariable=self.t2,width=10,relief='solid').grid(row=0,column=1)
        Button(self.addfm,text='add',width=8,command=lambda:self.addItem(self.t1.get(),self.t2.get(),'white')).grid(row=0,column=2)
        self.addfm.pack()
        self.fromFile('tags.txt')
    def addItem(self,left,right,color):
        tagKey[right]=(left,color)
        newFrame = Frame(self.fm,width=300)
        newFrame.key=right
        Label(newFrame,text=left,bg=color,relief='solid',width=10).grid(row=0,column=0)
        Label(newFrame,text=right,bg='white',relief='solid',width=10).grid(row=0,column=1)
        Button(newFrame,text='del',command=lambda:self.delItem(newFrame),width=8).grid(row=0,column=2)
        self.addfm.pack_forget()
        newFrame.pack()
        self.addfm.pack()
        self.t1.set('')
        self.t2.set('')
    def fromFile(self,filename):
        f = open(filename,'r')
        content = f.readlines()
        for item in content:
            detail = item.split()
            if len(detail)>=3:
                self.addItem(detail[0],detail[1],detail[2])
    def delItem(self,item):
        item.pack_forget()
        del tagKey[item.key]
        print(tagKey)
            
            
        
    
        


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

fm = tagFrame()
st = StringVar()
statLabel = Label(root,textvariable=st).place(x=1100,y=100)

def btclick():
    print(ib5.addTag('tagtagtag'))
    print(ib5.addTag('tag1'))
    print(ib5.addTag('tag2'))
def button2():
    for i in range(1,10):
        print(ib[i].pid)
        print(ib[i].creator)
        print(ib[i].typ)
        print(ib[i].imgpath)
def button3():
    for i in range(1,10):
        print(i)
        tg = list(ib[i].tags)
        print(tg)
        s = '|'.join(tg)
        print(s)
##Button(root,text='add tag',command=btclick).place(x=1100,y=200)
Button(root,text='button2',command=button2).place(x=1100,y=500)
Button(root,text='button3',command=button3).place(x=1100,y=600)

randomSet()
#root.update()
root.mainloop()

