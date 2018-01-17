import sqlite3
import random

conn = sqlite3.connect('./downdata.db')
cursor = conn.cursor()

def sqlInit():
    try:
        sql = '''CREATE TABLE download(uid text,username text,pid text,mode text,tag text)'''
        cursor.execute(sql)
    except:
        print("table exist")

def insert(uid,uname,pid,mode):
    try:
        sql = "INSERT INTO download VALUES('"+uid+"','"+uname+"','"+pid+"','"+mode+"','untagged')"
        cursor.execute(sql)
    except Exception as e:
        print(e)

def select(pid):
    sql = "SELECT * FROM download WHERE pid='"+pid+"'"
    res = cursor.execute(sql).fetchall()
    return res

def check(pid):
    res = select(pid)
    if len(res)==0:
        return False
    else:
        return True
    
def getUntag():
    sql = "SELECT * FROM download WHERE tag='untagged'"
    res = cursor.execute(sql).fetchall()
    return res

def randomGet():
    lst = getUntag()
    random.shuffle(lst)
    return lst[0:9]
    

def ci():
    conn.commit()
