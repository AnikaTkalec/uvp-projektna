import bottle
from bottle import route, run, template, static_file, redirect, request
from modeli import Baza, Pijaca


baza = Baza("stanje/ponudba.json", "stanje/racuni.json")
pijace = baza.preberi_pjace()
izbran_izpisek = {}
racun = []


@bottle.get("/")
def indeks():
    pijace1 = {}
    for pijaca in pijace:
        pijace1 |= pijaca.json()

    tipi_pijac = sorted({pijaca.tip_pijace for pijaca in pijace})

    znesek = 0
    for artikel in racun:
        znesek += artikel["cena"] * artikel["kolicina"]

    return template(
        "indeks",
        pijace=pijace1,
        tipi_pijac=tipi_pijac,
        racun_artikli=racun,
        racun_znesek=znesek,
    )


@bottle.post("/dodaj")
def dodaj():
    pijaca = request.forms.get("pijaca")
    for pijaca1 in racun:
        if pijaca1["artikel"] == pijaca:
            pijaca1["kolicina"] += 1
            return redirect("/")

    cena = 0
    for pijaca1 in pijace:
        if pijaca1.ime == pijaca:
            cena = pijaca1.prodajna_cena

    racun.append({"artikel": pijaca, "kolicina": 1, "cena": cena})

    return redirect("/")


@bottle.post("/zakljucek")
def zakljuci():
    global racun
    baza.shrani_racun(racun)
    racun = []

    return redirect("/")


@bottle.get("/izpiski")
def izpiski():
    global izbran_izpisek
    racuni = baza.preberi_racune()
    racuni_slovar = {}

    for e in racuni:
        racuni_slovar |= e.json()

    return template("izpiski", izpiski=racuni_slovar, izbran_izpisek=izbran_izpisek)


@bottle.post("/izpisek")
def izpisek():
    global izbran_izpisek
    racuni = baza.preberi_racune()

    zahtevan_racun = request.forms.get("stevilka-racuna")

    for e in racuni:
        if e.stevilka_racuna == zahtevan_racun:
            izbran_izpisek = e.json()
            izbran_izpisek_stevilka = list(izbran_izpisek)[0]
            izbran_izpisek = izbran_izpisek[list(izbran_izpisek)[0]]
            izbran_izpisek["stevilka_racuna"] = izbran_izpisek_stevilka

            break

    return redirect("/izpiski")


@route("/<filename:path>")
def send_static(filename):
    return static_file(filename, root="static/")


if __name__ == "__main__":
    run(host="localhost", port=8080)
