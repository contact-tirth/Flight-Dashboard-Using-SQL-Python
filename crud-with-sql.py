from ctypes import c_ushort

import pyodbc
try:
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=localhost\SQLEXPRESS;'
        r'DATABASE=DSMP;'
        r'Trusted_Connection=yes;',
        autocommit=True
    )

    cursor = conn.cursor()

    #cursor.execute('CREATE DATABASE DSMP')
    # conn.commit()
    print('Connection Established!')

except Exception as e:
    print(e)

#Create Table with Airpot
# cursor.execute("""CREATE TABLE airport(
#     a_id INTEGER PRIMARY KEY,
#     a_code VARCHAR(255) NOT NULL,
#     city VARCHAR(255) NOT NULL,
#     name VARCHAR(255) NOT NULL
#     )
# """)
# conn.commit()

#Insert Data
# cursor.execute("""
#     INSERT INTO airport VALUES
#     (1,'DEL','New Delhi','IGIA'),
#     (2,'CCU','Kolkata','NSCA'),
#     (3,'BOM','Bombay','CSMA')
# """)
# conn.commit()

#Update Data
cursor.execute("""UPDATE airport 
                  set city = 'Mumbai'
                  where a_id=3
                """)

#Delete
cursor.execute("DELETE FROM airport where a_id=3")
conn.commit()

#Retrive
cursor.execute("SELECT * FROM airport")
data=cursor.fetchall()
print(data)

cursor.close()
conn.close()