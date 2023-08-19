import mysql.connector
import PyPDF2
import re
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, sql, text
import os

conn = create_engine("mysql+mysqlconnector://root:mummyPAPPA1@127.0.0.1:3306/cvs")
cvs = []

folder = "CVS"
for file in os.listdir(folder):
    doc = PyPDF2.PdfFileReader(folder + "/" + file)
    pages = doc.getNumPages()
    info = []
    for i in range(pages):
        current_page = doc.getPage(i)
        text = current_page.extractText()
        info = text.split(': ')

    data = []
    for i in range(len(info)):
        data.append(info[i].split(' '))

    final = {}
    for i in range(0, 9):
        final[data[i][-1]] = ' '.join(data[i + 1][:-1])
    final[data[9][-1]] = ' '.join(data[10])
    cvs.append(final)

# Inserting pdf data into SQL Table
'''
df = pd.DataFrame(cvs)
df.to_sql(con=conn, name='resume', if_exists='replace', index=False,
          dtype={"Name": sqlalchemy.types.NVARCHAR(length=255),
                 "DOB": sqlalchemy.Date(),
                 "Phone": sqlalchemy.types.NVARCHAR(length=255),
                 "Email": sqlalchemy.types.NVARCHAR(length=255),
                 "Education": sqlalchemy.types.NVARCHAR(length=255),
                 "YOE": sqlalchemy.types.Integer(),
                 "Designation": sqlalchemy.types.NVARCHAR(length=255),
                 "Experience": sqlalchemy.types.NVARCHAR(length=500),
                 "Skills": sqlalchemy.types.NVARCHAR(length=255),
                 "Summary": sqlalchemy.types.NVARCHAR(length=900)})

'''

qu = "select * from resume where where yoe >= 20"

sql_query = sql.text(qu)
with conn.connect() as mysql_conn:
    df = pd.read_sql(sql_query, mysql_conn)

print(df.to_string())
