"""
ui_proste.py - gotowy interfejs do prostej wersji gry.
"""
import math
import customtkinter as ctk


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")




def utworz_okno(tytul="Dolomiti Bike"):
    """Tworzy glowne okno gry."""
    okno = ctk.CTk()
    okno.title(tytul)
    okno.geometry("950x700")
    return okno




def ekran_startowy(okno, on_start):
    """Wyswietla ekran startowy."""
    frame = ctk.CTkFrame(okno)
    frame.pack(fill="both", expand=True, padx=20, pady=20)


    ctk.CTkLabel(
        frame,
        text="DOLOMITI BIKE",
        font=ctk.CTkFont(size=48, weight="bold"),
    ).pack(pady=50)


    ctk.CTkLabel(
        frame,
        text="Wycieczka rowerowa przez Dolomity",
        font=ctk.CTkFont(size=20),
    ).pack(pady=10)


    ctk.CTkButton(
        frame,
        text="Rozpocznij wycieczke",
        font=ctk.CTkFont(size=18),
        width=250,
        height=50,
        command=on_start,
    ).pack(pady=30)


    return frame




def znajdz_szczyt_etapu(nazwa_etapu, szczyty):
    """Znajduje szczyt pasujacy do nazwy etapu."""
    if not szczyty:
        return None


    nazwa_lower = nazwa_etapu.lower()
    for szczyt in szczyty:
        nazwa_szczytu = szczyt["nazwa"].lower()
        if nazwa_lower in nazwa_szczytu or nazwa_szczytu in nazwa_lower:
            return szczyt


    return None




def ekran_wyboru(okno, etapy, szczyty, on_wybierz):
    """Wyswietla liste etapow do wyboru."""
    frame = ctk.CTkFrame(okno)
    frame.pack(fill="both", expand=True, padx=20, pady=20)


    ctk.CTkLabel(
        frame,
        text="Wybierz etap",
        font=ctk.CTkFont(size=28, weight="bold"),
    ).pack(pady=20)


    kolory = {"latwy": "green", "sredni": "orange", "trudny": "red"}


    for nr, etap in etapy.items():
        szczyt = znajdz_szczyt_etapu(etap["nazwa"], szczyty)
        info = ""
        if szczyt:
            info = f" - {szczyt['nazwa']} ({szczyt['wysokosc']}m)"


        ctk.CTkButton(
            frame,
            text=f"{nr}. {etap['nazwa']} - {etap['dystans']} km ({etap['trudnosc']}){info}",
            font=ctk.CTkFont(size=16),
            height=50,
            fg_color=kolory.get(etap["trudnosc"], "blue"),
            command=lambda n=nr: on_wybierz(n),
        ).pack(pady=5, padx=20, fill="x")


    return frame




def ekran_jazdy(okno, etap, stan, on_decyzja, pobliskie_szczyty=None):
    """Wyswietla ekran jazdy z trzema decyzjami gracza."""
    pobliskie_szczyty = pobliskie_szczyty or []


    frame = ctk.CTkFrame(okno)
    frame.pack(fill="both", expand=True, padx=20, pady=20)


    ctk.CTkLabel(
        frame,
        text=f"ETAP: {etap['nazwa']}",
        font=ctk.CTkFont(size=24, weight="bold"),
    ).pack(pady=10)


    ctk.CTkLabel(
        frame,
        text=f"Dystans: {etap['dystans']} km | Nachylenie: {etap['nachylenie']}% | Trudnosc: {etap['trudnosc']}",
        font=ctk.CTkFont(size=14),
        text_color="gray",
    ).pack(pady=5)


    srodek = ctk.CTkFrame(frame, fg_color="transparent")
    srodek.pack(fill="x", pady=15)


    canvas = ctk.CTkCanvas(srodek, width=620, height=250, bg="#87CEEB", highlightthickness=0)
    canvas.pack(side="left", padx=(0, 15))
    rysuj_trase(canvas, etap, stan)


    panel_szczytow = ctk.CTkFrame(srodek, width=230)
    panel_szczytow.pack(side="left", fill="both", expand=True)


    ctk.CTkLabel(
        panel_szczytow,
        text="Pobliskie szczyty z API",
        font=ctk.CTkFont(size=15, weight="bold"),
    ).pack(pady=(12, 8), padx=10)


    if pobliskie_szczyty:
        for szczyt in pobliskie_szczyty[:5]:
            tekst = (
                f"{szczyt['nazwa']}\n"
                f"{szczyt['wysokosc']} m, {szczyt['odleglosc']} km"
            )
            ctk.CTkLabel(
                panel_szczytow,
                text=tekst,
                font=ctk.CTkFont(size=12),
                justify="left",
                anchor="w",
            ).pack(fill="x", padx=12, pady=5)
    else:
        ctk.CTkLabel(
            panel_szczytow,
            text="Brak szczytow w poblizu albo brak danych z API.",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            wraplength=190,
        ).pack(padx=12, pady=20)


    panel = ctk.CTkFrame(frame)
    panel.pack(fill="x", padx=60, pady=10)


    pozycja = stan["pozycja"]
    dystans = etap["dystans"]
    ctk.CTkLabel(
        panel,
        text=f"Pozycja: {pozycja}/{dystans} km",
        font=ctk.CTkFont(size=18),
    ).pack(pady=5)
    ctk.CTkLabel(
        panel,
        text=f"Energia: {stan['energia']}%",
        font=ctk.CTkFont(size=18),
    ).pack(pady=5)
    ctk.CTkLabel(
        panel,
        text=f"Czas: {stan['czas']} min",
        font=ctk.CTkFont(size=18),
    ).pack(pady=5)


    przyciski = ctk.CTkFrame(frame, fg_color="transparent")
    przyciski.pack(pady=25)


    ctk.CTkButton(
        przyciski,
        text="Jedz dalej",
        width=160,
        height=45,
        command=lambda: on_decyzja("kontynuuj"),
    ).pack(side="left", padx=10)
    ctk.CTkButton(
        przyciski,
        text="Odpocznij",
        width=160,
        height=45,
        fg_color="green",
        command=lambda: on_decyzja("odpoczynek"),
    ).pack(side="left", padx=10)
    ctk.CTkButton(
        przyciski,
        text="Zjedz baton",
        width=160,
        height=45,
        fg_color="orange",
        command=lambda: on_decyzja("jedzenie"),
    ).pack(side="left", padx=10)


    return frame




def rysuj_gory(canvas):
    """Rysuje proste gory."""
    canvas.create_polygon(
        0, 200, 100, 100, 200, 170, 350, 80, 500, 150, 650, 90, 700, 200,
        fill="#9CA3AF",
        outline="",
    )
    canvas.create_polygon(
        0, 250, 120, 130, 250, 190, 400, 110, 550, 170, 700, 250,
        fill="#4B5563",
        outline="",
    )
    canvas.create_polygon(340, 80, 350, 60, 360, 80, fill="white", outline="")
    canvas.create_polygon(640, 90, 650, 70, 660, 90, fill="white", outline="")




def rysuj_rower(canvas, x, y):
    """Rysuje prostego rowerzyste."""
    canvas.create_oval(x - 8, y - 8, x + 8, y + 8, outline="#FFD700", width=2)
    canvas.create_oval(x + 16, y - 8, x + 32, y + 8, outline="#FFD700", width=2)
    canvas.create_line(x, y, x + 16, y - 12, fill="#FFD700", width=2)
    canvas.create_line(x + 16, y - 12, x + 24, y, fill="#FFD700", width=2)
    canvas.create_oval(x + 10, y - 30, x + 20, y - 20, fill="orange", outline="black")
    canvas.create_line(x + 15, y - 20, x + 15, y - 10, fill="blue", width=3)




def rysuj_trase(canvas, etap, stan):
    """Rysuje trase i aktualna pozycje rowerzysty."""
    canvas.delete("all")
    rysuj_gory(canvas)


    margin = 50
    szerokosc = int(canvas["width"])
    ground_y = 220
    dystans = etap["dystans"]
    nachylenie = etap["nachylenie"]


    punkty = []
    for i in range(dystans + 1):
        t = i / dystans
        x = margin + t * (szerokosc - 2 * margin)
        y = ground_y - 20 * math.sin(t * 6) - t * nachylenie * 3
        punkty.append((x, y))


    ziemia = list(punkty) + [(szerokosc - margin, ground_y + 20), (margin, ground_y + 20)]
    canvas.create_polygon([c for punkt in ziemia for c in punkt], fill="#8B7355", outline="")


    for i in range(len(punkty) - 1):
        canvas.create_line(
            punkty[i][0],
            punkty[i][1],
            punkty[i + 1][0],
            punkty[i + 1][1],
            fill="#4a90d9",
            width=4,
        )


    sx, sy = punkty[0]
    mx, my = punkty[-1]
    canvas.create_rectangle(sx - 8, sy - 20, sx + 8, sy, fill="green", outline="darkgreen")
    canvas.create_text(sx, sy + 12, text="START", fill="white", font=("Arial", 9, "bold"))
    canvas.create_rectangle(mx - 8, my - 20, mx + 8, my, fill="white", outline="black")
    canvas.create_text(mx, my + 12, text="META", fill="white", font=("Arial", 9, "bold"))


    pozycja = min(stan["pozycja"], dystans)
    rx, ry = punkty[int(pozycja)]
    rysuj_rower(canvas, rx - 12, ry)




def ekran_mety(okno, etap, wyniki, punkty, on_nastepny, on_menu):
    """Wyswietla ekran konca etapu."""
    frame = ctk.CTkFrame(okno)
    frame.pack(fill="both", expand=True, padx=20, pady=20)


    ctk.CTkLabel(
        frame,
        text="ETAP UKONCZONY!",
        font=ctk.CTkFont(size=36, weight="bold"),
        text_color="green",
    ).pack(pady=30)


    ctk.CTkLabel(frame, text=etap["nazwa"], font=ctk.CTkFont(size=24)).pack(pady=10)
    ctk.CTkLabel(frame, text=f"Czas: {wyniki['czas']} min", font=ctk.CTkFont(size=18)).pack(pady=5)
    ctk.CTkLabel(
        frame,
        text=f"Energia: {wyniki['energia']}%",
        font=ctk.CTkFont(size=18),
    ).pack(pady=5)
    ctk.CTkLabel(
        frame,
        text=f"PUNKTY: {punkty}",
        font=ctk.CTkFont(size=28, weight="bold"),
        text_color="gold",
    ).pack(pady=15)


    przyciski = ctk.CTkFrame(frame, fg_color="transparent")
    przyciski.pack(pady=30)


    ctk.CTkButton(przyciski, text="Nastepny etap", command=on_nastepny).pack(side="left", padx=10)
    ctk.CTkButton(przyciski, text="Menu glowne", fg_color="gray", command=on_menu).pack(side="left", padx=10)


    return frame




if __name__ == "__main__":
    okno = utworz_okno()
    ekran_startowy(okno, lambda: print("Start!"))
    okno.mainloop()
