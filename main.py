import psycopg2
from psycopg2 import sql

from random import randint
from typing import Optional

from pydantic import BaseModel, Field

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

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
with open("schema.sql", "r") as file:
    sql_script = file.read()
cur.execute(sql_script)
conn.commit()
print(" таблица сохранена")

app = FastAPI(openapi_prefix="/api/v1/")


class Car(BaseModel):
    model: str
    year: int = Field(ge=1700)
    color: str
    type: str



@app.post("/cars")
def cars_post(car: Car):

    id = randint(0, 999999)

    query = """
        INSERT INTO popova_chepelev.cars (id, model, car_year, color, type)
        VALUES (%s, %s, %s, %s, %s);
    """
    values = (id, car.model, car.year, car.color, car.type)

    cur.execute(query, values)
    conn.commit()

    return JSONResponse(
        status_code=200,
        content={
            "message": "succesful"
        }
    )


@app.get("/cars/{id}")
def cars_get(id: int):

    query = f"""
    SELECT * FROM popova_chepelev.cars WHERE id = {id}
    """
    response = cur.execute(query)
    print(response)

    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
