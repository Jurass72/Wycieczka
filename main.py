from game import utworz_okno, nowy_stan, ETAPY
from ui import utworz_okno
class Wycieczka:
    def __init__(self):
        self.okno = utworz_okno()
        self.frame = None
        self.stan = nowy_stan()
        self.etap = 1

        self.start()

if __name__ == "__main__":
    pass
