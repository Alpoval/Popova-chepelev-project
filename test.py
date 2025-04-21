import pytest
import psycopg2
import requests
from pydantic import BaseModel, Field
host = '79.174.88.238'
port = 15221
db_name = 'school_db'
user = 'school'
password = 'School1234*'

conn = psycopg2.connect(
    host=host,
    port=port,
    dbname=db_name,
    user=user,
    password=password

)

cur = conn.cursor()
print(" соединение с БД установлено")