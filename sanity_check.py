import psycopg2
import json

slodycze = None
paczki = []
with open("paczki.json", "r") as file:
    data = json.load(file)
    slodycze = data["slodycze"]
    for i in range(20):
        paczki += data[f"elf-{i}"]

ret = {}
for paczka in paczki:
    for produkt in paczka:
        if produkt in ret:
            ret[produkt] += 1
        else:
            ret[produkt] = 1

deficyt = 0
for k in ret:
    if int(slodycze[k]) < ret[k] :
        deficyt += ret[k] - int(slodycze[k])
print('deficyt', deficyt)
print('babeczki', int(slodycze['Babeczka śmietankowa']))
print('babeczki - deficyt', int(slodycze['Babeczka śmietankowa']) - deficyt)

conn = psycopg2.connect(
    host="192.168.56.56",
    database="test_db",
    user="windows",
    password="lalala123")

cur = conn.cursor()

#%%

# czy któregoś słodycza zostało mniej niż 0
cur.execute("SELECT * FROM slodycz_w_magazynie;")
slodycze_w_bazie = {}
results = list(cur.fetchall())
for res in results:
    if res[1] < 0:
        print("ERROR")
        print("SLODYCZ", res[0], "ILOSC", res[1])
    else :
        slodycze_w_bazie[res[0]] = res[1]

# czy suma w magazynie + w paczkach jest taka jak w magazynie na początku?
cur.execute("SELECT slodycz, SUM(ilosc) FROM slodycz_w_paczce GROUP BY slodycz;")
results2 = list(cur.fetchall())
for res in results2:
    slodycze_w_bazie[res[0]] = slodycze_w_bazie[res[0]] + res[1]

for s in slodycze:
    if int(slodycze[s]) != int(slodycze_w_bazie[s]):
        print("ERROR")
        print(s, "AT START", slodycze[s], "AT END", slodycze_w_bazie[s])



print("success")
cur.close()
conn.close()
