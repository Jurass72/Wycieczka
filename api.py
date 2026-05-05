import json
import math
import requests




def pobiez_szczyty():
    zapytanie = """
    [out: json][timeout: 25];
    node["natural"= "peak"]["name"](46.2, 11.5, 46.8, 12.5);
    outbody;
"""

    try:
        print("API pobieranie danych")
        request = requests.post(
            "https://overpass-api.de/api/interpreter",
            data = {"data": zapytanie},
            headers={"User-Agent": "DolomitiBikeApp/1.0 (contact@example.com)"},
            )
        request.raise_for_status()
        dane = request.json()
        szczyty = []
        for el in dane.get("elements", []):
            if el.get("type") == "node":
                tags = el.get("tags", {})
                ele = tags.get("ele", "0")
                try:
                    wysokosc = int(float(ele))
                except ValueError:
                    wysokosc = 0

                if wysokosc > 0:
                    szczyty.append({
                    "id":el.get("id"),
                    "nazwa":tags.get("name", "Nieznany"),
                    "wysokosc": wysokosc,
                    "lat":el.get("lat"),
                    "lon":el.get("lon"),

                    })
                        
        print(f"[OK] Pobrano {len(szczyty)} szczytów")
        return szczyty

    except Exception as e:
        print(f"Błąd - {e}")
        return []
        

if __name__ == "__main__":
    szczyty = pobiez_szczyty()
    for szczyt in szczyty:
        print(f"{szczyt['Nazwa']} - {['wysokosc']}m ")








        #do githuba dodac
        