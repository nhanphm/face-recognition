import sqlite3

def initDatabase():
    conn=sqlite3.connect("FaceBase.db")
    cmd = "CREATE TABLE IF NOT EXISTS People (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, Name TEXT)"
    conn.execute(cmd)
    conn.commit()
    conn.close()

def insertOrUpdate(Id,Name):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM People WHERE user_id="+str(Id)
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE People SET Name='"+str(Name)+"' WHERE user_id="+str(Id)
    else:
        cmd="INSERT INTO People Values(null, "+str(Id)+", '"+str(Name)+"')"
        print(cmd)

    conn.execute(cmd)
    conn.commit()
    conn.close()

#get data from sqlite by ID
def getProfile(id):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM People WHERE user_id="+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile
