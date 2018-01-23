import downloadData as dd
import data as dt

def printl(lst):
    print('size:',len(lst))
    for item in lst:
        print(item)

printl(dd.getTag())
printl(dt.getAll())
