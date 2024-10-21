import mysql.connector 
import os
import shutil

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="userdata"
    )

mycursor = mydb.cursor()

#mycursor.execute("CREATE TABLE passdata (id INTEGER, username VARCHAR(20), password VARCHAR(20))")

#encrypting the password
def enc(s):
    p=""
    for i in s:
        p=p+chr(ord(i)+5)
    return p

#check if username exists
def username(s):
    flag=False
    mycursor.execute("SELECT username FROM passdata")
    usernames=mycursor.fetchall()
    for i in usernames:
        if i[0]==s:
            flag=True
            break
    return flag

#sign in
def signup():
    while True:
        s=input("Enter username: ")
        if username(s):
            print("Username already exists. ")
        else:
            break
    pwd=input("Enter password: ")
    mycursor.execute("SELECT MAX(id) FROM passdata")
    count=mycursor.fetchone()[0]
    t=(count+1,s,enc(pwd))
    p="INSERT INTO passdata(id, username, password) VALUES(%s,%s,%s)"
    mycursor.execute(p,t)
    mydb.commit()
    return s

#login
def login():
    s=input("Enter username: ")
    if username(s):
        pwd=input("Enter password: ")
        mycursor.execute("SELECT password FROM passdata WHERE username=%s",(s,))
        enc_pyd=mycursor.fetchone()[0]
        if enc(pwd)==enc_pyd:
            print("Login successful")
            return s
        else:
            print("Incorrect password")
    else:
        print("Username does not exist")

#delete account
def delete():
    s=input("Enter username: ")
    if username(s):
        pwd=input("Enter password: ")
        mycursor.execute("SELECT password FROM passdata WHERE username=%s",(s,))
        enc_pyd=mycursor.fetchone()[0]
        if enc(pwd)==enc_pyd:
            mycursor.execute("DELETE FROM passdata WHERE username=%s",(s,))
            mydb.commit()
            return s
        else:
            print("Incorrect password")
    else:
        print("Username does not exist")


#FILE MANAGEMENT

def createdir(directory_name,parent_path):
    path=os.path.join(parent_path,directory_name)
    os.mkdir(path)

def deletedir(directory_name,parent_path):
    path=os.path.join(parent_path,directory_name)
    shutil.rmtree(path)

def createfile(file_name,path):
    filepath=os.path.join(path,file_name+".txt")
    if os.path.isfile(filepath):
        print("File already exists!")
    else:
        f=open(filepath,"w+")
        print("File created!")
        f.close()

def editfile(text,file_name,path):
    filepath=os.path.join(path,file_name+".txt")
    if not os.path.isfile(filepath):
        print("File does not exist!")
    else:
        with open(file_name, "a") as f:
            f.write(text)
            f.close()
        print("File edited!")

def renamefile(old_name,new_name,path):
    oldpath=os.path.join(path,old_name+".txt")
    if not os.path.isfile(oldpath):
        print("File does not exist!")
    else:
        newpath=os.path.join(path,new_name+".txt")
        os.rename(oldpath,newpath)
        print("File renamed!")

def deletefile(file_name,path):
    filepath=os.path.join(path,file_name+".txt")
    if not os.path.isfile(filepath):
        print("File does not exist!")
    else:
        os.remove(filepath)
        print("File deleted!")

#operations
s=int(input("Enter 1 to add account, 2 to delete account and 3 to login to an existing account: "))
if s==1:
    username=signup()
    parent_path="D:/Education/"
    createdir(username,parent_path)
elif s==2:
    username=delete()
    parent_path="D:/Education/"
    try:
        deletedir(username,parent_path)
    except:
        print()   
               
elif s==3:
    username=login()
    try:
        parent_dir="D:/Education"
        path=os.path.join(parent_dir,username,"")
        n=int(input("Enter: 1)to create new file 2)to edit existing file 3)to rename existing file 4)to delete a file"))
        name=input("Enter file name:")
        if n==1:
            createfile(name,path)
        elif n==2:
            text=input("Enter text you want to add")
            editfile(text,name,path)
        elif n==3:
            newname=input("Enter new file name:")
            renamefile(name,newname,path)
        elif n==4:
            deletefile(name,path)
        else:
            print("Wrong operation!")
    except:
        print()
else:
    print("Wrong operation!")

