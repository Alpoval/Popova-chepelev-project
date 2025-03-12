import psycopg2
from psycopg2 import sql
host = '79.174.88.238'
port=15221
db_name='school_db'
user='school'
password='School1234*'

conn = psycopg2.connect(
  host=host,
  port=port,
  dbname=db_name,
  user=user,
  password=password

)

cbs=conn.cursor()
print(" соединение с БД установлено")
with open("schema.sql","r") as file:
  sql_script=file.read()
cbs.execute(sql_script)
conn.commit()
print(" таблица сохранена")

