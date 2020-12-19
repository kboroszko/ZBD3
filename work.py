import psycopg2

#%%

# BEGIN;

conn = psycopg2.connect(
    host="192.168.56.56",
    database="test_db",
    user="windows",
    password="lalala123")

cur = conn.cursor()

#%%
#  -- tworzymy paczkę
# INSERT INTO paczka (...) RETURNING id;
cur.execute("INSERT INTO paczka (kraj, opis) VALUES (%s, %s) RETURNING id;", ('Polska', 'bla bla bla'))
paczka_id = cur.fetchone()[0]

#%%
# > 1 -- identyfikator paczki
# -- sprawdzamy czy w magazynie jest wystarczająco dużo słodyczy z pierwszej pozycji na liście(Czekolada Studencka * 2)
# SELECT ilosc_pozostalych FROM slodycz_w_magazynie WHERE nazwa = 'Czekolada Studencka';
#%%

# -- nie ma dwóch czekolad, więc sprawdzamy do czego jest podobna czekolada studencka
# SELECT .... FROM podobny_slodycz...


# > Milka, 0.9
# -- sprawdzamy czy jest wystarczająco dużo Milki w magazynie
# SELECT id, ilosc_pozostalych FROM slodycz_w_magazynie WHERE nazwa = 'Milka';



# > 20 -- liczba Milek w magazynie
# -- dodajemy do zamówienia dwie milki i zmniejszamy stan w magazynie
# INSERT INTO slodycz_w_paczce (1, 'Milka', 2);

# UPDATE slodycz_w_magazynie SET ilosc_pozostalych = ilosc_pozostalych - 2 WHERE nazwa = 'Milka';
# -- przechodzimy do kolejnej pozycji w liście
# ....
# COMMIT;
