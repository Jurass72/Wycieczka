import random
ETAPY = {
    1:{"nazwa": "Cortina",
        "dystans": 15,
        "nachylenie": 7,
        "trudnosc": "łatwy", 
        "coords": (46.540, 12.135),
},
2:{"nazwa": "Marmolada",
        "dystans": 12,
        "nachylenie": 10,
        "trudnosc": "średni", 
        "coords": (46.45, 11.85)
},
}
def nowy_stan():
    return {"energia": 100, "pozycja": 0, "czas": 0, "etap": 1}

def generuj_przystanki(szczyty, dystans):
    przystanki = []

    if not szczyty:
        return przystanki
    ile = min(5,len(szczyty))
    for i, szczyt in enumerate(szczyty[:ile]):
        baza = dystans * (i + 1) / (ile + 1)
        km = baza * random.uniform(0.85, 1.15)
        km = max(1, min(dystans-1,km))
        przystanki.append({
            "km":round(km, 2),
            "szczyt" : szczyt,
            "odkryty" : False,
            "aktywny": False
        })

    return przystanki


def oblicz_czas(dystans, nachylenie, energia):
    predkosc = 20 - (nachylenie * 2)
    predkosc *= (0.5+0.5*energia/100)
    predkosc = max(predkosc, 5)
    return int(dystans/predkosc)



def aktualizuj_stan(stan, decyzja, etap):
    nowy = stan.copy()


    if decyzja == "odpoczynek":
        nowy["energia"] = min(100, nowy["energia"] + 20)
        nowy["czas"] += 20

    elif decyzja == "jedzenie":
        nowy["energia"] = min(100, nowy["energia"] + 15)
        nowy["czas"] += 5
    elif decyzja == "kontynuuj":
        nowy["energia"] = max(0, nowy["energia"] - etap["nachylenie"] * 2 )
        nowy["czas"] += oblicz_czas(1, etap["nachylenie"], nowy["energia"])
        nowy["pozycja"] += 1

    return nowy



def czy_koniec(stan, etap):
    if stan["energia"] <= 0:
        return True, "brakuje energii"
    if stan["pozycja"] >= etap["dystans"]:
        return True, "META"
    return False, ""

#odpalic te funklcje (if __name__) w tym pliku  







