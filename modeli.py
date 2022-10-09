import json
from os.path import exists
from datetime import datetime


class Pijaca:
    def __init__(self, ime, tip_pijace, nabavna_cena, prodajna_cena):
        self.tip_pijace = tip_pijace
        self.ime = ime
        self.nabavna_cena = nabavna_cena
        self.prodajna_cena = prodajna_cena

    def json(self):
        return {
            self.ime: {
                "tip_pijace": self.tip_pijace,
                "nabavna_cena": self.nabavna_cena,
                "prodajna_cena": self.prodajna_cena,
            }
        }


class Racuni:
    def __init__(self, stevilka_racuna, artikli, dobicek, datum, ime_lokala):
        self.stevilka_racuna = stevilka_racuna
        self.artikli = artikli
        self.datum = datum
        self.ime_lokala = ime_lokala
        self.znesek = sum(
            [artikel["cena"] * artikel["kolicina"] for artikel in artikli]
        )
        self.dobicek = dobicek

    def json(self):
        return {
            self.stevilka_racuna: {
                "artikli": self.artikli,
                "datum": self.datum,
                "ime_lokala": self.ime_lokala,
                "znesek": self.znesek,
                "dobicek": self.dobicek,
            }
        }


class Baza:
    def __init__(self, ime_datoteke_pijace, ime_datoteke_racuni):
        self.ime_datoteke_pijace = ime_datoteke_pijace
        self.ime_datoteke_racuni = ime_datoteke_racuni

    def preberi(self, ime_datoteke):
        if not exists(ime_datoteke):
            raise Exception
        else:
            file = open(ime_datoteke, "r", encoding="UTF-8")
            res = json.load(file)
            file.close()
            return res

    def shrani(self, ime_datoteke, podatki):
        file = open(ime_datoteke, "w", encoding="UTF-8")
        json.dump(podatki, file)
        file.close()

    def preberi_pjace(self):
        return [
            Pijaca(
                ime_pijace,
                podatki["tip_pijace"],
                podatki["nabavna_cena"],
                podatki["prodajna_cena"],
            )
            for ime_pijace, podatki in self.preberi(self.ime_datoteke_pijace).items()
        ]

    def shrani_pijace(self, pijace):
        pijace1 = {}
        for pijaca in pijace:
            pijace1 |= pijaca.json()

        self.shrani(self.ime_datoteke_pijace, pijace1)

    def preberi_racune(self):
        return [
            Racuni(
                stevilka_racuna,
                podatki["artikli"],
                podatki["dobicek"],
                podatki["datum"],
                podatki["ime_lokala"],
            )
            for stevilka_racuna, podatki in self.preberi(
                self.ime_datoteke_racuni
            ).items()
        ]

    def shrani_racune(self, racuni):
        racuni1 = {}
        for racun in racuni:
            racuni1 |= racun.json()

        self.shrani(self.ime_datoteke_racuni, racuni1)

    def shrani_racun(self, racun):
        racuni = self.preberi_racune()
        pijace = self.preberi_pjace()

        if len(racuni) == 0:
            zadnji_id = 1
        else:
            zadnji_id = max([int(racun1.stevilka_racuna) for racun1 in racuni])
            zadnji_id += 1

        datum = datetime.now()

        dobicek = 0
        for x in racun:
            for k in pijace:
                if k.ime == x["artikel"]:
                    dobicek = (k.prodajna_cena - k.nabavna_cena) * x["kolicina"]

        racuni.append(
            Racuni(zadnji_id, racun, dobicek, datum.strftime("%d/%m/%Y %H:%M"), "Lokal")
        )

        self.shrani_racune(racuni)
