import data as d
import os

try:
    os.remove("./test.db")
except:
    print("remove error")

d.sqlInit()

d.insert('p001','c01','single','t1 t2 t3','3')#1
d.insert('p002','c01','single','t1'      ,'2')#2
d.insert('p003','c01','single','t2 t1 t3','2')#3
d.insert('p010','c03','single','t3 t2 t1','0')#4
d.insert('p011','c02','single','t1 t3'   ,'0')#5
d.insert('p021','c02','single','t1 t2 t3','1')#6
d.insert('x000','c03','set'   ,'t1 t2 t3','3')#7
d.insert('x010','c05','single','t2'      ,'3')#8
d.insert('p021','c02','single','t1 t2 t3','4')#9

r1 = d.search(['t1'])
print(r1)
r2 = d.search([],[],[2,3])
print(r2)
r3 = d.search(['t1'],['c02'],[1])
print(r3)
r4 = d.search(['t1','t2'])
print(r4)
r5 = d.search([],[],[3])
print(r5)
r6 = d.search([],['c03'])
print(r6)
