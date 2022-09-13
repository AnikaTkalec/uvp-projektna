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
                


