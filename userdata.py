import mysql.connector 
mydb=mysql.connector.connect(
	host="localhost",
	user="root",
	password="localhost"
)

mycursor=mydb.cursor()

mycursor.execute("CREATE DATABASE userdata")