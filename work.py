import psycopg2
import json
import sys
from psycopg2 import extensions
#%%
def get_ilosci(paczka):
    ret = {}
    for produkt in paczka:
        if produkt in ret:
            ret[produkt] += 1
        else:
            ret[produkt] = 1
    return ret


#%%
# id = 0
id = int(sys.argv[1])
paczki = None
with open("paczki.json", "r") as file:
    data = json.load(file)
    paczki = data[f"elf-{id}"]

print("elf", id, "paczki", len(paczki))

#%%
# BEGIN;

conn = psycopg2.connect(
    host="192.168.56.56",
    database="test_db",
    user="windows",
    password="lalala123")

conn.set_isolation_level(extensions.ISOLATION_LEVEL_SERIALIZABLE)

cur = conn.cursor()

#%%
wyciagniete = {}
def wyciagnij(nazwa, ilosc):
    if nazwa in wyciagniete:
        wyciagniete[nazwa] = ilosc + wyciagniete[nazwa]
    else:
        wyciagniete[nazwa] = ilosc

counter = 0
kupa = False
for p in paczki:
    paczka = get_ilosci(p)
    #  -- tworzymy paczkę
    # INSERT INTO paczka (...) RETURNING id;
    cur.execute("INSERT INTO paczka (kraj, opis) VALUES (%s, %s) RETURNING id;", ('Polska', 'bla bla bla'))
    paczka_id = cur.fetchone()[0]


    # > 1 -- identyfikator paczki
    for produkt in paczka:
    # -- sprawdzamy czy w magazynie jest wystarczająco dużo słodyczy z pierwszej pozycji na liście(Czekolada Studencka * 2)
    # SELECT ilosc_pozostalych FROM slodycz_w_magazynie WHERE nazwa = 'Czekolada Studencka';
        cur.execute('SELECT ilosc_pozostalych FROM slodycz_w_magazynie WHERE nazwa = %s;', (produkt,))
        ilosc = cur.fetchone()[0]
        wybrany = ""
        if ilosc < paczka[produkt]:
            print("zamieniam")
            # -- nie ma dwóch czekolad, więc sprawdzamy do czego jest podobna czekolada studencka
            # SELECT .... FROM podobny_slodycz...
            cur.execute('SELECT podobny_do FROM podobny_slodycz WHERE ktory_slodycz = %s AND podobienstwo > 0;', (produkt,))
            for (res,) in cur.fetchall():
                cur.execute('SELECT ilosc_pozostalych FROM slodycz_w_magazynie WHERE nazwa = %s;', (res,))
                ilosc_podobnego = cur.fetchone()[0]
                if ilosc_podobnego >= paczka[produkt]:
                    wybrany = res
                    break
        else:
            wybrany = produkt

        if wybrany == "":
            kupa = True
            print("KUPA, PACZKA", paczka_id, "NIEUDANA!", paczka)
            print("brakowalo", produkt)
            conn.rollback()
            break
        # -- dodajemy do zamówienia dwie milki i zmniejszamy stan w magazynie
        # INSERT INTO slodycz_w_paczce (1, 'Milka', 2);
        # UPDATE slodycz_w_magazynie SET ilosc_pozostalych = ilosc_pozostalych - 2 WHERE nazwa = 'Milka';

        cur.execute("INSERT INTO slodycz_w_paczce VALUES (%s, %s, %s);", (paczka_id, wybrany, paczka[produkt]))
        cur.execute("UPDATE slodycz_w_magazynie SET ilosc_pozostalych = ilosc_pozostalych - %s WHERE nazwa=%s", (paczka[produkt],wybrany))
        wyciagnij(wybrany, paczka[produkt])
    if kupa:
        print("elf",id, 'skonczyl', counter, 'paczek')
        break
    else:
        conn.commit()
        counter += 1

print(f'elf-{id},ile_paczek,{len(paczki)},ile_ok,{counter},ile_zle,{len(paczki) - counter}')
cur.close()
conn.close()