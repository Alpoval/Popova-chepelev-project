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

with open("schema.sql", "r") as file:
    sql_script = file.read()
cur.execute(sql_script)
conn.commit()


BASE_URL= 'http://0.0.0.0:8080'

class Car(BaseModel):
    model: str
    year: int = Field(ge=1700)
    color: str
    type: str


@pytest.fixture(autouse=True)
def cleanup():
    cur.execute("DELETE FROM popova_chepelev.cars")
    yield


def test_post_car():
    test_data= {
        'model':" BMV X5",
        'year': 2024,
        'color': "red",
        'type': 'SUV'
    }

    response=requests.post(f"{BASE_URL}cars",json=test_data)

    if  response.status_code != 200:
        raise ValueError("bad")

    db_data = cur.execute( "SELECT model,car_year,color,type FROM popova_chepelev.cars",fetch=True)

    if  len(db_data)!=1:
        raise ValueError("bad")
    if db_data[0][0] != test_data ["model"]:
        raise ValueError("bad")


def test_get_cars():
    test_data = (1,"porshe",2024,'black',"cabrio")
    cur.execute("INSERT INTO popova_chepelev.cars (id,model,car_year,color,type) "
                "VALUES (%s,%s,%s,%s,%s",test_data)

    response = requests.get(f"{BASE_URL}cars")

    if response.status_code !=200:
        raise ValueError("bad")
    if len(response.json())!=1:
        raise ValueError("bad")


def test_put_car():
    test_data = (1,"hyundai solaris",2020,"brown",'sedan')
    cur.execute("INSERT INTO popova_chepelev.cars (id,model,car_year,color,type) "
                "VALUES (%s,%s,%s,%s,%s",test_data)
    update_data={
        'model':"hyundai sonata",
        'year':2019,
        'color':'black',
        'type':'coupe'
    }

    response=requests.put(f"{BASE_URL}cars/1", json=update_data)

    if response.status_code !=200:
        raise ValueError("bad")

    db_data=cur.execute( "SELECT model FROM popova_chepelev.cars WHERE id=1", fetch=True)

    if db_data[0][0] != update_data["model"]:
        raise ValueError("bad")


def test_delete_car():
    test_data = (1,"Mazda 7",2019,'red','CUV')
    cur.execute("INSERT INTO popova_chepelev.cars (id,model,car_year,color,type) "
                "VALUES (%s,%s,%s,%s,%s",test_data)

    response=requests.delete(f"{BASE_URL}cars/1")

    if response.status_code !=200:
        raise ValueError("bad")

    db_data = cur.execute("SELECT model FROM popova_chepelev.cars WHERE id=1", fetch=True)

    if len(db_data) !=0:
        raise ValueError("bad")

