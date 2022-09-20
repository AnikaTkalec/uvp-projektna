import json
from os.path import exists


class Natakar:

    stevec = None
    natakarji = {}

    def __init__(self, ime, priimek, uporabnisko_ime, geslo):
        self.id = None
        self.ime = ime
        self.priimek = priimek
        self.uporabnisko_ime = uporabnisko_ime
        self.geslo = geslo

    def shrani(self):
        if self.id is not None:
            raise ValueError("self.id ni None, ne morem shraniti")
        if Natakar.stevec is None:
            raise ValueError('Natakarji še niso naloženi')
        self.id = Natakar.stevec
        Natakar.stevec += 1
        Natakar.natakarji[self.id] = self
        with open("stanje/natakarji.json", "w", encoding="UTF-8") as datoteka:
            natakarji = []
            for natakar in Natakar.natakarji.values():
                natakarji.append(
                    {
                        "id": natakar.id,
                        "ime": natakar.ime,
                        "priimek": natakar.priimek,
                        "uporabnisko_ime": natakar.uporabnisko_ime,
                        "geslo": natakar.geslo,
                    }
                )
            datoteka.write(json.dumps(natakarji))

def nalozi_natakarje():
    if not exists("stanje/natakarji.json"):
        Natakar.stevec = 1
    else:
        with open("stanje/natakarji.json", "r", encoding="UTF-8") as datoteka:
            natakarji = json.loads(datoteka.read())
            najvecji_id = 0
            for natakar in natakarji:
                Natakar.natakarji[natakar['id']] = Natakar(natakar['ime'], natakar['priimek'], natakar['uporabnisko_ime'], natakar['geslo'])
                Natakar.natakarji[natakar['id']].id = natakar['id']
                if natakar['id'] > najvecji_id:
                    najvecji_id = natakar['id']
            Natakar.stevec = najvecji_id + 1
                
class Pijaca:

    stevec = None
    pijace = {}


    def __init__(self, tip_pijace, ime, kolicina, cena):
        self.id = None
        self.tip_pijace = tip_pijace
        self.ime = ime
        self.kolicina = kolicina
        self.cena = cena

    
    def shrani(self):
        if self.id is not None:
            raise ValueError("self.id ni None, ne morem shraniti")
        if Pijaca.stevec is None:
            raise ValueError('Pijače še niso naložene')
        self.id = Pijaca.stevec
        Pijaca.stevec += 1
        Pijaca.pijace[self.id] = self
        with open("stanje/pijace.json", "w", encoding="UTF-8") as datoteka:
            pijace = []
            for pijaca in Pijaca.pijace.values():
                pijace.append(
                    {
                        "id": pijaca.id,
                        "tip_pijace": pijaca.tip_pijace,
                        "ime": pijaca.ime,
                        "kolicina": pijaca.kolicina,
                        "cena": pijaca.cena,
                    }
                )
            datoteka.write(json.dumps(pijace))

def nalozi_pijace():
    if not exists("stanje/pijace.json"):
        Pijaca.stevec = 1
    else:
        with open("stanje/pijace.json", "r", encoding="UTF-8") as datoteka:
            pijace = json.loads(datoteka.read())
            najvecji_id = 0
            for pijaca in pijace:
                Pijaca.pijace[pijaca['id']] = Natakar(pijaca['tip_pijace'], pijaca['ime'], pijaca['kolicina'], pijaca['cena'])
                Pijaca.pijace[pijaca['id']].id = pijaca['id']
                if pijaca['id'] > najvecji_id:
                    najvecji_id = pijaca['id']
            Pijaca.stevec = najvecji_id + 1





