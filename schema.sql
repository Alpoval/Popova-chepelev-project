CREATE SCHEMA IF NOT EXISTS popova_chepelev;
CREATE TABLE  IF NOT EXISTS popova_chepelev.cars (
  id INTEGER PRIMARY KEY,
  model TEXT NOT NULL,
  car_year INTEGER NOT NULL,
  color TEXT NOT NULL,
  type TEXT NOT NULL
);
