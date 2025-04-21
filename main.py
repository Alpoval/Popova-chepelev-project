from http.client import HTTPException
import psycopg2
from random import randint
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

    car.id = randint(0, 999999)

    query = """
        INSERT INTO popova_chepelev.cars (id, model, car_year, color, type)
        VALUES (%s, %s, %s, %s, %s);
    """
    values = (car.id, car.model, car.year, car.color, car.type)

    cur.execute(query, values)
    conn.commit()

    return JSONResponse(
        status_code=200,
        content={
            "message": "succesful"
        }
    )


@app.get("/cars")
def cars_get():

    cur.execute( "SELECT id, model, car_year, color, type FROM  popova_chepelev.cars ")
    cars = cur.fetchall()
    return [{
        "id": car[0],
        "model": car[1],
        "year": car[2],
        "color":car[3],
        "type": car[4]
        } for car in cars]
@app.put("/cars/{car.id}")
def cars_update(car_id: int, car:Car):
    cur.execute("SELECT id FROM popova_chepelev.cars WHERE id=%s", car_id,)

    if not cur.fetchone():
        raise HTTPException(status_code=404,detail="Car not found")

    query="""UPDATE popova_chepelev.cars 
                SET model =%s,car_year=%s,color=%s,type=%s
                WHERE id=%s;"""
    values=(car.model,car.year,car.color,car.type,car.id)
    cur.execute(query,values)
    conn.commit()

    return {"message":"Updated"}
@app.delete("/cars/{car.id}")
def car_delete(car_id:int):
    cur.execute("SELECT id FROM popova_chepelev.cars WHERE id=%s", car_id, )

    if not cur.fetchone():
        raise HTTPException(status_code=404,detail="Car not found")

    cur.execute("DELETE FROM popova_chepelev.cars WHERE id=%s", car_id, )

    conn.commit()

    return {"message":"Deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
