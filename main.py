from game import nowy_stan, ETAPY
from ui import utworz_okno, ekran_jazdy, ekran_startowy, ekran_wyboru
from api import pobierz_szczyty

okno = utworz_okno()
frame = None
stan = nowy_stan()
etap = 1
szczyty = []

def wyczysc():
    global frame

    if frame:
        frame.destroy()
        frame = None

def start():
    global frame
    wyczysc()
    frame = ekran_startowy(okno, wybor)

def wybor():
    global frame, szczyty

    wyczysc()
    if not szczyty:
        print("Pobieram szxczyty z API")
        szczyty = pobierz_szczyty()
        print(f"Liczba pobranych szczytow: {len(szczyty)}")


    frame = ekran_wyboru(okno, ETAPY, szczyty, graj)

def graj(nr):
    global etap_nr, stan\
    
    etap_nr = nr
    stan = nowy_stan()
    jazda()


def jazda():
    global frame
    

    wyczysc()
    etap = ETAPY[etap_nr]
    lat, lon = etap["coords"]
    obok = None
    frame = ekran_jazdy(okno, etap, stan, decyzja, obok)

def decyzja(co):
    pass

if __name__ == "__main__":
    start()
    okno.mainloop()
    czy_koniec()
