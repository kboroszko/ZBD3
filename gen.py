import sys
import random
import numpy as np
from matplotlib import pyplot as plt


POPULATE_FILE = 'populate.sql'
PACZKI_FILE = 'paczki.json'

random.seed(12345)

slodycze = '''Babeczka śmietankowa
Babka biszkoptowa
Baton Bounty
Baton Knoppers
Baton Mars
Baton Milky Way
Baton Snickers
Baton Twix
Biszkopty
Budyń
Chałwa
Ciasto francuskie
Ciasto z kruszonką
Cukier biały
Cukier trzcinowy
Cukierki
Czekolada biała
Czekolada gorzka
Czekolada mleczna
Czekolada nadziewana
Delicje
Drożdżówka
Dżem niskosłodzony
Dżem wysokosłodzony
Eklerki czekoladowe
Eklerki z bitą śmietaną
Eklerki z kremem
Ferrero Rocher
Galaretka owocowa
Herbatnik
Irysy (cukierki)
Jagodzianka
Jeżyki, ciasteczka
Karmelek
Keks owocowy
Kisiel
Landrynki
Lody bakaliowe
Lody czekoladowe
Lody orzechowe
Lody owocowe
Lody śmietankowe
Lody waniliowe
M&M's
Markizy, ciasteczka
Miód naturalny pszczeli
Napoleonka
Nutella
Pączek
Pieguski
Pierniki czekoladowe
Ptasie mleczko
Ptyś z bitą śmietaną
Raffaello
Rolada biszkoptowa z dżemem
Rolada warszawska
Sernik wiedeński
Syrop truskawkowy
Szarlotka
Toffifee
Wafle nadziewane'''.replace('\'', "").split('\n')

#%%

ILOSC_ELFOW = 20
n=len(slodycze)
podobienstwa = np.random.rand(n,n)
podobienstwa[podobienstwa > 0.982] = 1
podobienstwa[podobienstwa < 0.999] = 0

for i in range(n):
    for j in range(n):
        if podobienstwa[i,j] == 1 :
            podobienstwa[j,i] = 1

plt.matshow(podobienstwa)
#%%
ilosci = 75 + (np.random.rand(n)*25).astype(np.int)

fig, ax = plt.subplots()

x = np.arange(n)
rects1 = ax.bar(x, ilosci, 0.45, label='ilosci')
ax.set_xticks(x)
ax.set_xticklabels(slodycze, rotation='vertical')
plt.subplots_adjust(bottom=0.35)

#%%
print('srednio:', np.mean(ilosci))
print('najwiecej', slodycze[np.argmax(ilosci)], np.max(ilosci))
print('najwiecej', slodycze[np.argmin(ilosci)], np.min(ilosci))


#%%
per_paczka = 10
total = np.sum(ilosci)
prob = ilosci/total
paczki = []

n_paczek = int(total/per_paczka) - 95
for i in range(n_paczek):
    paczka = []
    while len(paczka) < 10:
        los = random.randint(0,n-1)
        paczka.append(slodycze[los])
    paczki.append(paczka)



def indexof(szukany):
    for i,s in enumerate(slodycze):
        if s == szukany:
            return i
    return -1

wyniki = np.zeros((n))
for paczka in paczki:
    for s in paczka:
        i = indexof(s)
        if i < 0 :
            print("\n\nERROR!\n\n")
        wyniki[i] += 1

print(np.sum(wyniki), np.sum(ilosci))

print(wyniki > ilosci)
#%%
import codecs

with codecs.open(POPULATE_FILE, "w+", "utf-8") as file:
    file.write("\\c test_db;\n\n")
    for s,i in zip(slodycze,ilosci):
        file.write(f"INSERT INTO slodycz_w_magazynie VALUES ('{s}',{i});\n")
    file.write("\n\n")
    for i,row in enumerate(podobienstwa[:]):
        slodycz = slodycze[i]
        for j,v in enumerate(row):
            podobny_do = slodycze[j]
            if v == 1 and i != j:
                file.write(f"INSERT INTO podobny_slodycz VALUES ('{slodycz}','{podobny_do}', {random.random()});\n")



#%%
import json
#%%

paczki_json = {}
ppe = int(len(paczki)/ILOSC_ELFOW)

for i in range(ILOSC_ELFOW):
    paczki_json[f"elf-{i}"] = paczki[i:min(len(paczki), ppe*(i+1))]

paczki_json["slodycze"] = {}
for slodycz,ilosc in zip(slodycze, ilosci):
    paczki_json["slodycze"][slodycz] = str(ilosc)

with codecs.open(PACZKI_FILE, "w+", "utf-8") as file:
    file.write(json.dumps(paczki_json))

