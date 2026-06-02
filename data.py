import json
def sortuj_wysokosc(szczyty, malejaco = True):
    return sorted(szczyty, key = lambda x: x.get("wysokosc", 0), reverse =  malejaco)

def filtruj_wysokosc(szczyty, min_wys):
    return [s for s in szczyty if s.get("wysokosc", 0) >= min_wys]

def statystyki(szczyty):
    if not szczyty:
        return{"liczba":0, "średnia":0, "min":0, "max":0}
    wysokosc = [s.get("wysokosc", 0) for s in szczyty]
    return{
        "liczba": len(wysokosc),
        "średnia": sum(wysokosc) // len(wysokosc),
        "min": min(wysokosc),
        "max": max(wysokosc)
    }

def zapisz_pliku(szczyty, nazwa="szczyty.json"):
    with open(nazwa, "w", encoding="utf-8") as f:
        json.dump(szczyty, f, indent=4, ensure_ascii=False)

def odczytaj_pliku(nazwa="szczyty.json"):
    with open(nazwa, "r", encoding="utf-8") as f:
        return json.load(f)


#zrobic funlcje do zapisywania pliku json lub txt
#2 funkcja do odczytywania pliku