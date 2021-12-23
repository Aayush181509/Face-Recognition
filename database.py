import mysql.connector as conn

mydb = conn.connect(
    host="localhost",
    user="root",
    password="mysql@123",
    database="mydatabase"
)
# print(mydb)
mycursor = mydb.cursor()
# mycursor.execute("Create table attendance(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) , time VARCHAR(255))")
# # for x in mycursor:
sql = "INSERT INTO attendance (name, time) VALUES (%s, %s)"
val = [
  ('Aayush', '2021-06-10')
  ]

mycursor.executemany(sql, val)

mydb.commit()
