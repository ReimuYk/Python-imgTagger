import sqlite3

conn = sqlite3.connect('./tagdata.db')
cursor = conn.cursor()

def sqlInit():
    try:
        sql = '''CREATE TABLE pxv(pid text,creator text,type text,tags text,hmode text)'''
        cursor.execute(sql)
    except:
        print("table exist")

# input 5 string
def insert(pid,creator,typ,tagString,hmode):
    try:
        sql = "INSERT INTO pxv VALUES ('"+pid+"','"+creator+"','"+typ+"','"+tagString+"','"+hmode+"')"
        cursor.execute(sql)
    except Exception as e:
        print(e)

# tags(list),creators(list)
def search(tags,creators=[],hmode=[0,1,2,3,4]):
    sql = "SELECT * FROM pxv WHERE ("
    for i in range(len(tags)):
        s="(tags LIKE '%"+tags[i]+"%') "
        if i!=0:
            sql = sql+"AND "
        sql = sql+s
    if len(tags)!=0:
        sql = sql+") AND ("
    for i in range(len(hmode)):
        s="hmode='"+str(hmode[i])+"'"
        if i!=0:
            sql = sql+" OR "
        sql = sql+s
    if len(creators)!=0:
        sql = sql+") AND ("
    for i in range(len(creators)):
        s="creator='"+creators[i]+"'"
        if i!=0:
            sql = sql+" OR "
        sql = sql+s
    sql = sql+")"
    res = cursor.execute(sql)
    return res.fetchall()

def getAll():
    sql = "SELECT * FROM pxv"
    res = cursor.execute(sql).fetchall()
    return res
    

def ci():
    conn.commit()
    

##sql = '''CREATE TABLE data(tag1 text,id int)'''
##sql = '''INSERT INTO data VALUES ('line1',111)'''
##cursor.execute(sql)
##
##cursor.execute('''INSERT INTO data VALUES('line2',222)''')

