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

BASE_URL= 'http://0.0.0.0:8080'
class Car(BaseModel):
    model: str
    year: int = Field(ge=1700)
    color: str
    type: str


@pytest.fixture(autouse=True)
def cleanup():
    execute_query("DELETE FROM popova_chepelev.cars")
    yield
def test_post_car():
    test_data= {
        'model':" BMV X5",
        'year': 2024,
        'color': "red",
        'type': 'crossover'
    }
    response=requests.post(f"{BASE_URL}cars",json=test_data)
    assert response.status_code == 200

    db_data = execute_query( "SELECT model,car_year,color,type FROM popova_chepelev.cars",fetch=True)

    assert len(db_data)==1
    assert db_data[0][0] == test_data ["model"]


