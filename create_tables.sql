;
\c test_db;

CREATE TABLE slodycz_w_magazynie
    (nazwa VARCHAR,
    ilosc_pozostalych INT CHECK ( ilosc_pozostalych >= 0 ));

CREATE TABLE paczka
    (Id INT GENERATED ALWAYS AS IDENTITY,
    kraj VARCHAR,
    opis VARCHAR);

CREATE TABLE slodycz_w_paczce
    (paczka_Id INT,
    slodycz VARCHAR,
    ilosc INT);

CREATE TABLE podobny_slodycz
    (ktory_slodycz VARCHAR,
    podobny_do VARCHAR,
    podobienstwo FLOAT);
