import _json
import math
import request




def pobiez_szczyty():
    zapytanie = """
    [out: json][timeout: 25];
    node["natural"= "peak"]["name"](146.2, 11.5, 46.8, 12.5);
    outbody;
"""

    try:
        print("API pobieranie danych")
        request = requests.post("https://overpass-api.de/api/interpreter", data = {"data": zapytanie})
        request.raise_for_status()
        dane = request.json()
        szczyty = []
        for el in dane.get("elements", []):
            pass


    except Exception as e:
        print(f"Błąd - {e}")
        return []\
        










        #do githuba dodac
        