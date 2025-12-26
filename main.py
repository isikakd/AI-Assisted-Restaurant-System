import tkinter as tk
from collections import Counter
from itertools import combinations

FONT_TITLE = ("Arial", 28, "bold")
FONT_SECTION = ("Arial", 18, "bold")
FONT_ITEM = ("Arial", 16)
FONT_ENTRY = ("Arial", 16)
FONT_BUTTON = ("Arial", 17, "bold")
FONT_RESULT = ("Arial", 20, "bold")

BG_MAIN = "#f4f6f8"
BG_HEADER = "#1f2933"
BG_DRINKS = "#e6f4ff"
BG_DESSERTS = "#fff6d5"

gecmis_siparisler = [
    ["Latte", "Cheesecake"],
    ["Latte", "Brownie"],
    ["Espresso", "Brownie"],
    ["Çikolatalı Kek", "Türk Kahvesi"],
    ["Latte", "Çikolatalı Kek"],
    ["Milkshake", "Brownie"],
    ["Latte", "Türk Kahvesi"],
    ["Espresso", "Cheesecake"]
]

def modeli_egit(veri):
    model = Counter()
    for siparis in veri:
        for a, b in combinations(siparis, 2):
            model[(a, b)] += 1
            model[(b, a)] += 1
    return model

def ai_oneri(siparisler, model):
    alinan = [u for u, a in siparisler if a > 0]
    skorlar = Counter()
    for urun in alinan:
        for (a, b), skor in model.items():
            if a == urun and b not in alinan:
                skorlar[b] += skor
    if skorlar:
        return f"AI Recommendation: {skorlar.most_common(1)[0][0]}"
    return "AI Recommendation: No suggestion available"

urunler = {
    "Latte": 120,
    "Espresso": 100,
    "Iced Latte": 170,
    "Milkshake": 200,
    "Çay": 70,
    "Su": 25,
    "Matcha": 220,
    "Türk Kahvesi": 120,
    "Dibek Kahvesi": 150,
    "Cheesecake": 230,
    "Çikolatalı Kek": 150,
    "Brownie": 180,
    "Vişneli Kek": 200
}

icecekler = [
    "Latte", "Espresso", "Iced Latte", "Milkshake",
    "Çay", "Su", "Matcha", "Türk Kahvesi", "Dibek Kahvesi"
]

tatlilar = [
    "Cheesecake", "Çikolatalı Kek", "Brownie", "Vişneli Kek"
]

root = tk.Tk()
root.title("AI Restaurant Management System")
root.geometry("1200x720")
root.configure(bg=BG_MAIN)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

header = tk.Label(
    root,
    text="AI-Assisted Restaurant Ordering System",
    font=FONT_TITLE,
    bg=BG_HEADER,
    fg="white",
    pady=18
)
header.grid(row=0, column=0, columnspan=2, sticky="ew")

secimler = {}
adetler = {}

def urunleri_ciz(frame, liste, bg):
    for i, urun in enumerate(liste):
        secimler[urun] = tk.IntVar()
        adetler[urun] = tk.Entry(frame, width=6, font=FONT_ENTRY)
        tk.Checkbutton(
            frame,
            text=urun,
            variable=secimler[urun],
            bg=bg,
            font=FONT_ITEM
        ).grid(row=i, column=0, sticky="w", pady=6)
        adetler[urun].grid(row=i, column=1, sticky="e", pady=6, padx=10)

icecek_frame = tk.LabelFrame(
    root,
    text=" Drinks",
    font=FONT_SECTION,
    bg=BG_DRINKS,
    padx=25,
    pady=25
)
icecek_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
icecek_frame.grid_columnconfigure(0, weight=1)

tatli_frame = tk.LabelFrame(
    root,
    text=" Desserts",
    font=FONT_SECTION,
    bg=BG_DESSERTS,
    padx=25,
    pady=25
)
tatli_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
tatli_frame.grid_columnconfigure(0, weight=1)

urunleri_ciz(icecek_frame, icecekler, BG_DRINKS)
urunleri_ciz(tatli_frame, tatlilar, BG_DESSERTS)

def hesapla():
    toplam = 0
    siparisler = []
    for urun, fiyat in urunler.items():
        if secimler.get(urun) and secimler[urun].get():
            adet = int(adetler[urun].get() or 0)
            toplam += adet * fiyat
            siparisler.append((urun, adet))
    sonuc_label.config(text=f"Total: {toplam} TL")
    oneri_label.config(text=ai_oneri(siparisler, ai_model))

buton = tk.Button(
    root,
    text="CALCULATE TOTAL",
    font=FONT_BUTTON,
    bg="#2ecc71",
    fg="black",
    padx=30,
    pady=12,
    command=hesapla
)
buton.grid(row=2, column=0, columnspan=2, pady=18)

oneri_label = tk.Label(
    root,
    text="",
    font=FONT_ITEM,
    fg="blue",
    bg=BG_MAIN
)
oneri_label.grid(row=3, column=0, columnspan=2)

sonuc_label = tk.Label(
    root,
    text="Total: 0 TL",
    font=FONT_RESULT,
    bg=BG_MAIN
)
sonuc_label.grid(row=4, column=0, columnspan=2, pady=10)

ai_model = modeli_egit(gecmis_siparisler)
root.mainloop()
