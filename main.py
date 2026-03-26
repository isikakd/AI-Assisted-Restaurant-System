"""
Café POS — AI-Assisted Restaurant Ordering System
Light theme · Advanced AI engine · Full-featured sidebar
"""
import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter, defaultdict
from itertools import combinations
import datetime
import math

from styles import (
    BG_MAIN, BG_CARD, BG_CARD2, BG_SIDEBAR, BG_HEADER, BG_INPUT,
    ACCENT, ACCENT_LIGHT, ACCENT_HOVER,
    SUCCESS, SUCCESS_LIGHT, DANGER, DANGER_LIGHT,
    WARNING, WARNING_LIGHT, INFO, INFO_LIGHT,
    TEXT_H, TEXT_B, TEXT_SEC, TEXT_MUTED, TEXT_INV,
    BORDER, BORDER_MED, BORDER_DARK,
    CAT_ACCENT, CAT_LIGHT, CAT_TAB_BG,
    FONT_HERO, FONT_TITLE, FONT_SECTION, FONT_ITEM, FONT_ITEM_B,
    FONT_SMALL, FONT_SMALL_B, FONT_PRICE, FONT_ENTRY,
    FONT_BTN, FONT_BTN_SM, FONT_TOTAL, FONT_AI, FONT_BADGE, FONT_MONO,
)

# ══════════════════════════════════════════════════════════════════════════════
#  MENU
# ══════════════════════════════════════════════════════════════════════════════
MENU = {
    # ── İçecekler
    "Latte":              {"price": 120, "emoji": "☕", "cat": "drink",   "popular": True},
    "Espresso":           {"price": 100, "emoji": "☕", "cat": "drink",   "popular": False},
    "Cappuccino":         {"price": 130, "emoji": "☕", "cat": "drink",   "popular": True},
    "Flat White":         {"price": 140, "emoji": "☕", "cat": "drink",   "popular": False},
    "Iced Latte":         {"price": 170, "emoji": "🧊", "cat": "drink",   "popular": True},
    "Soğuk Brew":         {"price": 190, "emoji": "🧊", "cat": "drink",   "popular": False},
    "Milkshake":          {"price": 200, "emoji": "🥤", "cat": "drink",   "popular": True},
    "Çay":                {"price":  70, "emoji": "🍵", "cat": "drink",   "popular": True},
    "Bitki Çayı":         {"price":  90, "emoji": "🌿", "cat": "drink",   "popular": False},
    "Su":                 {"price":  25, "emoji": "💧", "cat": "drink",   "popular": False},
    "Matcha Latte":       {"price": 220, "emoji": "🍵", "cat": "drink",   "popular": False},
    "Türk Kahvesi":       {"price": 120, "emoji": "☕", "cat": "drink",   "popular": True},
    "Dibek Kahvesi":      {"price": 150, "emoji": "☕", "cat": "drink",   "popular": False},
    "Limonata":           {"price": 110, "emoji": "🍋", "cat": "drink",   "popular": True},
    "Portakal Suyu":      {"price": 100, "emoji": "🍊", "cat": "drink",   "popular": False},
    "Sıcak Çikolata":     {"price": 160, "emoji": "🍫", "cat": "drink",   "popular": True},
    # ── Tatlılar
    "Cheesecake":         {"price": 230, "emoji": "🍰", "cat": "dessert", "popular": True},
    "Çikolatalı Kek":     {"price": 150, "emoji": "🍫", "cat": "dessert", "popular": True},
    "Brownie":            {"price": 180, "emoji": "🟫", "cat": "dessert", "popular": True},
    "Vişneli Kek":        {"price": 200, "emoji": "🍒", "cat": "dessert", "popular": False},
    "Tiramisu":           {"price": 250, "emoji": "🍮", "cat": "dessert", "popular": True},
    "Waffle":             {"price": 220, "emoji": "🧇", "cat": "dessert", "popular": True},
    "Profiterol":         {"price": 210, "emoji": "🍡", "cat": "dessert", "popular": False},
    "Dondurma":           {"price": 130, "emoji": "🍨", "cat": "dessert", "popular": False},
    "Sufle":              {"price": 260, "emoji": "🍮", "cat": "dessert", "popular": False},
    "Künefe":             {"price": 280, "emoji": "🧀", "cat": "dessert", "popular": True},
    # ── Yiyecekler
    "Tost":               {"price": 140, "emoji": "🥪", "cat": "food",    "popular": True},
    "Kumpir":             {"price": 280, "emoji": "🥔", "cat": "food",    "popular": True},
    "Sandviç":            {"price": 220, "emoji": "🥙", "cat": "food",    "popular": True},
    "Patates Kızartması": {"price": 130, "emoji": "🍟", "cat": "food",    "popular": True},
    "Salata":             {"price": 180, "emoji": "🥗", "cat": "food",    "popular": False},
    "Krep":               {"price": 160, "emoji": "🥞", "cat": "food",    "popular": False},
    "Menemen":            {"price": 200, "emoji": "🍳", "cat": "food",    "popular": True},
    "Avokado Toast":      {"price": 240, "emoji": "🥑", "cat": "food",    "popular": False},
    "Sahanda Yumurta":    {"price": 150, "emoji": "🍳", "cat": "food",    "popular": False},
    "Çorba":              {"price": 130, "emoji": "🍲", "cat": "food",    "popular": False},
    # ── Günün Özel Menüsü
    "Özel Pasta":         {"price": 320, "emoji": "🎂", "cat": "special", "popular": False},
    "Şef Tatlısı":        {"price": 290, "emoji": "⭐", "cat": "special", "popular": True},
    "Günün Çorbası":      {"price": 160, "emoji": "🍲", "cat": "special", "popular": False},
    "Sezonluk İçecek":    {"price": 180, "emoji": "🌸", "cat": "special", "popular": True},
    "Özel Kahvaltı":      {"price": 350, "emoji": "🌅", "cat": "special", "popular": False},
}

CATEGORIES = {
    "drink":   ("🥤 İçecekler",    "drink"),
    "dessert": ("🍰 Tatlılar",     "dessert"),
    "food":    ("🍽  Yiyecekler",  "food"),
    "special": ("⭐ Günün Menüsü", "special"),
}

# ══════════════════════════════════════════════════════════════════════════════
#  TRAINING DATA  —  100 realistic orders
# ══════════════════════════════════════════════════════════════════════════════
GECMIS = [
    ["Latte","Cheesecake"],["Latte","Brownie"],["Espresso","Brownie"],
    ["Çikolatalı Kek","Türk Kahvesi"],["Latte","Çikolatalı Kek"],
    ["Milkshake","Brownie"],["Latte","Türk Kahvesi"],["Espresso","Cheesecake"],
    ["Matcha Latte","Cheesecake"],["Iced Latte","Vişneli Kek"],
    ["Dibek Kahvesi","Brownie"],["Cappuccino","Tiramisu"],["Latte","Waffle"],
    ["Tost","Çay"],["Kumpir","Limonata"],["Sandviç","Latte"],
    ["Menemen","Türk Kahvesi"],["Avokado Toast","Iced Latte"],
    ["Salata","Limonata"],["Krep","Latte"],["Waffle","Cappuccino"],
    ["Tiramisu","Espresso"],["Özel Pasta","Latte"],["Günün Çorbası","Tost"],
    ["Latte","Profiterol"],["Türk Kahvesi","Künefe"],["Flat White","Cheesecake"],
    ["Sıcak Çikolata","Waffle"],["Türk Kahvesi","Sufle"],["Espresso","Tiramisu"],
    ["Cappuccino","Brownie"],["Iced Latte","Cheesecake"],["Milkshake","Waffle"],
    ["Çay","Tost"],["Latte","Sandviç"],["Portakal Suyu","Menemen"],
    ["Limonata","Salata"],["Türk Kahvesi","Çikolatalı Kek"],["Latte","Krep"],
    ["Espresso","Brownie"],["Dibek Kahvesi","Künefe"],["Cappuccino","Cheesecake"],
    ["Soğuk Brew","Cheesecake"],["Matcha Latte","Vişneli Kek"],
    ["Sıcak Çikolata","Brownie"],["Flat White","Tiramisu"],
    ["Türk Kahvesi","Brownie"],["Latte","Tiramisu"],["Espresso","Cheesecake"],
    ["Iced Latte","Brownie"],["Cappuccino","Waffle"],["Milkshake","Çikolatalı Kek"],
    ["Çay","Sandviç"],["Kumpir","Çay"],["Patates Kızartması","Limonata"],
    ["Menemen","Çay"],["Sahanda Yumurta","Türk Kahvesi"],["Çorba","Tost"],
    ["Avokado Toast","Latte"],["Krep","Sıcak Çikolata"],["Salata","Latte"],
    ["Tost","Latte"],["Sandviç","Çay"],["Kumpir","Latte"],
    ["Şef Tatlısı","Espresso"],["Sezonluk İçecek","Cheesecake"],
    ["Günün Çorbası","Sandviç"],["Özel Kahvaltı","Latte"],
    ["Latte","Dondurma"],["Türk Kahvesi","Dondurma"],["Espresso","Profiterol"],
    ["Cappuccino","Profiterol"],["Milkshake","Dondurma"],
    ["Bitki Çayı","Cheesecake"],["Bitki Çayı","Vişneli Kek"],
    ["Limonata","Cheesecake"],["Portakal Suyu","Waffle"],
    ["Su","Sandviç"],["Su","Tost"],["Su","Salata"],
    ["Flat White","Brownie"],["Soğuk Brew","Tiramisu"],
    ["Matcha Latte","Brownie"],["Sıcak Çikolata","Cheesecake"],
    ["Latte","Avokado Toast"],["Iced Latte","Salata"],
    ["Cappuccino","Çikolatalı Kek"],["Türk Kahvesi","Tiramisu"],
    ["Espresso","Künefe"],["Dibek Kahvesi","Sufle"],
    ["Latte","Sufle"],["Cappuccino","Künefe"],
    ["Şef Tatlısı","Latte"],["Sezonluk İçecek","Waffle"],
    ["Özel Pasta","Espresso"],["Günün Çorbası","Çay"],
]

# ══════════════════════════════════════════════════════════════════════════════
#  DISCOUNT CODES
# ══════════════════════════════════════════════════════════════════════════════
DISCOUNT_CODES = {
    "HOSGELDIN": 10,
    "MUTLUCAFE":  15,
    "VIP2024":    20,
    "TATLI":       5,
    "OGRENCI":    12,
    "HAFTA":       8,
}

# ══════════════════════════════════════════════════════════════════════════════
#  AI ENGINE  —  Co-occurrence + confidence + category diversity + popularity
# ══════════════════════════════════════════════════════════════════════════════
class AIEngine:
    """
    Advanced item-to-item recommendation engine.

    Scoring formula:
        raw_score      = co-occurrence count
        confidence     = P(B|A) = count(A,B) / count(A)  [lift-style]
        category_bonus = +20% if suggestion is from underrepresented category
        popularity_bonus = +10% if item is marked popular
        final_score    = raw_score * confidence_weight + bonuses
    """

    def __init__(self, orders: list):
        self.pair_counts   = Counter()   # (a,b) -> count
        self.item_counts   = Counter()   # a -> total appearances
        self.total_orders  = len(orders)

        for order in orders:
            for item in order:
                self.item_counts[item] += 1
            for a, b in combinations(order, 2):
                self.pair_counts[(a, b)] += 1
                self.pair_counts[(b, a)] += 1

    def _confidence(self, a: str, b: str) -> float:
        """P(B | A) — how often B appears given A was ordered."""
        if self.item_counts[a] == 0:
            return 0.0
        return self.pair_counts[(a, b)] / self.item_counts[a]

    def _popularity_score(self, name: str) -> float:
        """Normalised global frequency."""
        total = sum(self.item_counts.values()) or 1
        return self.item_counts[name] / total

    def suggest(self, current_order: list[tuple], top_n: int = 3):
        """
        Return list of (name, emoji, confidence_pct, reason) tuples.
        current_order: [(name, qty), ...]
        """
        selected = [n for n, q in current_order if q > 0]
        if not selected:
            return []

        selected_cats = {MENU[n]["cat"] for n in selected if n in MENU}
        scores = {}

        for candidate in MENU:
            if candidate in selected:
                continue

            raw   = sum(self.pair_counts[(s, candidate)] for s in selected)
            conf  = max(self._confidence(s, candidate) for s in selected)
            pop   = self._popularity_score(candidate)

            # category diversity bonus
            cand_cat = MENU[candidate]["cat"]
            cat_bonus = 0.15 if cand_cat not in selected_cats else 0.0

            # popularity bonus
            pop_bonus = 0.10 if MENU[candidate].get("popular") else 0.0

            final = raw * (1 + conf) + (cat_bonus + pop_bonus) * raw
            if final > 0:
                scores[candidate] = (final, conf, cand_cat)

        top = sorted(scores.items(), key=lambda x: x[1][0], reverse=True)[:top_n]

        result = []
        for name, (score, conf, cat) in top:
            conf_pct = min(99, round(conf * 100))
            # build human-readable reason
            triggers = [s for s in selected if self.pair_counts[(s, name)] > 0]
            if triggers:
                reason = f"{triggers[0]} ile sıklıkla tercih edilir"
            elif MENU[name].get("popular"):
                reason = "Müşteriler arasında popüler"
            else:
                reason = "Menüyü tamamlar"
            result.append((name, MENU[name]["emoji"], conf_pct, reason))
        return result

    def category_stats(self) -> dict:
        """Return order-share per category for the analytics panel."""
        cat_counts = Counter()
        for (a, _), cnt in self.pair_counts.items():
            if a in MENU:
                cat_counts[MENU[a]["cat"]] += cnt
        total = sum(cat_counts.values()) or 1
        return {k: round(v / total * 100) for k, v in cat_counts.items()}

    def top_items(self, n=5) -> list:
        return [(name, cnt) for name, cnt in self.item_counts.most_common(n) if name in MENU]


# ══════════════════════════════════════════════════════════════════════════════
#  WIDGET: MenuRow
# ══════════════════════════════════════════════════════════════════════════════
class MenuRow(tk.Frame):
    def __init__(self, parent, name, info, on_change=None, **kw):
        bg = BG_CARD
        super().__init__(parent, bg=bg, **kw)
        self.name       = name
        self.qty        = tk.IntVar(value=0)
        self._selected  = tk.BooleanVar(value=False)
        self._on_change = on_change
        cat             = info["cat"]
        cat_col         = CAT_ACCENT[cat]

        # left color stripe
        tk.Frame(self, bg=cat_col, width=3).pack(side="left", fill="y")

        # hidden variable — checkbox removed, stepper drives selection

        # emoji + name
        name_frame = tk.Frame(self, bg=bg)
        name_frame.pack(side="left", fill="x", expand=True, padx=(4, 8))
        tk.Label(name_frame, text=f"{info['emoji']}  {name}",
                 font=FONT_ITEM, bg=bg, fg=TEXT_H, anchor="w").pack(side="left")
        if info.get("popular"):
            tk.Label(name_frame, text=" ★ ",
                     font=FONT_BADGE, bg=ACCENT_LIGHT, fg=ACCENT,
                     padx=4, pady=1).pack(side="left", padx=4)

        # stepper
        stepper = tk.Frame(self, bg=bg)
        stepper.pack(side="left")

        self._btn_minus = tk.Button(
            stepper, text="−", font=("Helvetica", 12, "bold"),
            bg=BG_INPUT, fg=TEXT_SEC, bd=0, padx=8, pady=2,
            activebackground=DANGER_LIGHT, activeforeground=DANGER,
            command=self._decrement, cursor="hand2",
        )
        self._btn_minus.pack(side="left")

        self._qty_lbl = tk.Label(
            stepper, textvariable=self.qty, font=FONT_PRICE,
            bg=BG_INPUT, fg=TEXT_H, width=3, anchor="center",
        )
        self._qty_lbl.pack(side="left")

        self._btn_plus = tk.Button(
            stepper, text="+", font=("Helvetica", 12, "bold"),
            bg=BG_INPUT, fg=TEXT_SEC, bd=0, padx=8, pady=2,
            activebackground=SUCCESS_LIGHT, activeforeground=SUCCESS,
            command=self._increment, cursor="hand2",
        )
        self._btn_plus.pack(side="left")

        # price
        tk.Label(
            self, text=f"₺{info['price']}",
            font=FONT_PRICE, bg=bg, fg=cat_col, width=7, anchor="e",
        ).pack(side="right", padx=(0, 12))

    def _notify(self):
        if self._on_change:
            self._on_change()

    def _on_toggle(self):
        if not self._selected.get():
            self.qty.set(0)
        self._notify()

    def _increment(self):
        self._selected.set(True)
        self.qty.set(self.qty.get() + 1)
        self._notify()

    def _decrement(self):
        v = self.qty.get()
        if v > 1:
            self.qty.set(v - 1)
        elif v == 1:
            self.qty.set(0)
            self._selected.set(False)
        self._notify()

    def get_order(self):
        return self.name, self.qty.get() if self._selected.get() else 0

    def reset(self):
        self._selected.set(False)
        self.qty.set(0)


# ══════════════════════════════════════════════════════════════════════════════
#  SIMPLE PROGRESS BAR (pure tkinter)
# ══════════════════════════════════════════════════════════════════════════════
class MiniBar(tk.Canvas):
    def __init__(self, parent, color, **kw):
        kw.setdefault("height", 6)
        kw.setdefault("bd", 0)
        kw.setdefault("highlightthickness", 0)
        kw.setdefault("bg", BORDER)
        super().__init__(parent, **kw)
        self._color = color
        self._bar   = self.create_rectangle(0, 0, 0, 6, fill=color, outline="")

    def set(self, pct: float):
        self.update_idletasks()
        w = self.winfo_width()
        self.coords(self._bar, 0, 0, w * max(0, min(1, pct)), 6)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════════════════════════════════════
class RestaurantApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CAFE")
        self.geometry("1380x900")
        self.minsize(1100, 760)
        self.configure(bg=BG_MAIN)
        self.resizable(True, True)

        self._rows          = {}
        self._order_history = []
        self._discount_pct  = 0
        self._ai            = AIEngine(GECMIS)

        self._style_ttk()
        self._build_ui()

    # ── ttk styling ───────────────────────────────────────────────────────────
    def _style_ttk(self):
        s = ttk.Style()
        s.theme_use("default")
        s.configure("TNotebook",       background=BG_MAIN,  borderwidth=0)
        s.configure("TNotebook.Tab",   background=BG_CARD2, foreground=TEXT_SEC,
                    font=FONT_ITEM_B,  padding=[14, 8],    borderwidth=0)
        s.map("TNotebook.Tab",
              background=[("selected", BG_CARD)],
              foreground=[("selected", TEXT_H)])
        s.configure("TScrollbar", background=BORDER_MED, troughcolor=BG_CARD2,
                    arrowcolor=TEXT_MUTED, borderwidth=0, gripcount=0)
        s.configure("TCombobox",  fieldbackground=BG_INPUT, background=BG_INPUT,
                    foreground=TEXT_H, font=FONT_SMALL)

    # ══════════════════════════════════════════════════════════════════════════
    #  LAYOUT
    # ══════════════════════════════════════════════════════════════════════════
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=0, minsize=340)
        self.grid_rowconfigure(1, weight=1)
        self._build_header()
        self._build_menu_area()
        self._build_sidebar()
        self._build_statusbar()

    # ── Header ────────────────────────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self, bg=BG_HEADER)
        hdr.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Brand
        brand = tk.Frame(hdr, bg=BG_HEADER)
        brand.pack(side="left", padx=24, pady=14)
        tk.Label(brand, text="☕  CAFE", font=FONT_HERO,
                 bg=BG_HEADER, fg="#FEF3C7").pack(side="left")


        # Right controls
        right = tk.Frame(hdr, bg=BG_HEADER)
        right.pack(side="right", padx=20)

        tk.Label(right, text="Masa:", font=FONT_SMALL_B,
                 bg=BG_HEADER, fg="#A8A29E").pack(side="left", padx=(0, 4))
        self._masa_var = tk.StringVar(value="Masa 1")
        masa_cb = ttk.Combobox(
            right, textvariable=self._masa_var,
            values=[f"Masa {i}" for i in range(1, 21)] + ["Paket Servis", "Bar", "Teras"],
            width=12, font=FONT_SMALL, state="readonly",
        )
        masa_cb.pack(side="left", padx=(0, 20))

        self._clock_lbl = tk.Label(right, font=FONT_MONO, bg=BG_HEADER, fg="#78716C")
        self._clock_lbl.pack(side="left")
        self._tick()

    def _tick(self):
        now = datetime.datetime.now().strftime("%H:%M:%S  |  %d.%m.%Y")
        self._clock_lbl.config(text=now)
        self.after(1000, self._tick)

    # ── Menu area ─────────────────────────────────────────────────────────────
    def _build_menu_area(self):
        container = tk.Frame(self, bg=BG_MAIN)
        container.grid(row=1, column=0, sticky="nsew", padx=(12, 6), pady=12)
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Search bar
        search_row = tk.Frame(container, bg=BG_MAIN)
        search_row.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        tk.Label(search_row, text="🔍", font=("Helvetica", 13),
                 bg=BG_MAIN, fg=TEXT_SEC).pack(side="left")
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", self._on_search)
        tk.Entry(search_row, textvariable=self._search_var, font=FONT_ENTRY,
                 bg=BG_CARD, fg=TEXT_H, insertbackground=TEXT_H,
                 relief="flat", bd=0, highlightthickness=1,
                 highlightbackground=BORDER_MED, highlightcolor=ACCENT,
                 ).pack(side="left", fill="x", expand=True, ipady=6, padx=(6, 0))

        # Notebook
        self._notebook = ttk.Notebook(container)
        self._notebook.grid(row=1, column=0, sticky="nsew")
        self._tab_rows = {}   # cat_key -> {name: MenuRow}

        for cat_key, (cat_label, _) in CATEGORIES.items():
            tab_frame, body = self._make_tab(cat_key)
            self._notebook.add(tab_frame, text=f"  {cat_label}  ")
            self._tab_rows[cat_key] = {}
            items = {k: v for k, v in MENU.items() if v["cat"] == cat_key}
            for name, info in items.items():
                row = MenuRow(body, name, info, on_change=self._live_update)
                row.pack(fill="x", pady=1)
                tk.Frame(body, bg=BORDER, height=1).pack(fill="x", padx=8)
                self._rows[name] = row
                self._tab_rows[cat_key][name] = row

    def _make_tab(self, cat_key):
        color = CAT_ACCENT.get(cat_key, ACCENT)
        tab_frame = tk.Frame(self._notebook, bg=BG_MAIN)
        tab_frame.grid_rowconfigure(1, weight=1)
        tab_frame.grid_columnconfigure(0, weight=1)

        tk.Frame(tab_frame, bg=color, height=3).grid(row=0, column=0, columnspan=2, sticky="ew")

        canvas = tk.Canvas(tab_frame, bg=BG_CARD2, bd=0, highlightthickness=0)
        vsb = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        canvas.grid(row=1, column=0, sticky="nsew")
        vsb.grid(row=1, column=1, sticky="ns")

        body = tk.Frame(canvas, bg=BG_CARD2)
        bid  = canvas.create_window((0, 0), window=body, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(bid, width=e.width))
        body.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        return tab_frame, body

    def _on_search(self, *_):
        q = self._search_var.get().strip().lower()
        for cat_key, rows in self._tab_rows.items():
            for name, row in rows.items():
                if q and q not in name.lower():
                    row.pack_forget()
                else:
                    row.pack(fill="x", pady=1)

    # ── Sidebar ───────────────────────────────────────────────────────────────
    def _build_sidebar(self):
        sb = tk.Frame(self, bg=BG_SIDEBAR, bd=0)
        sb.grid(row=1, column=1, sticky="nsew", padx=(0, 12), pady=12)
        sb.grid_columnconfigure(0, weight=1)
        sb.grid_rowconfigure(3, weight=1)

        # ── Order header
        oh = tk.Frame(sb, bg=BG_SIDEBAR)
        oh.grid(row=0, column=0, sticky="ew", padx=14, pady=(12, 4))
        tk.Label(oh, text="📋  Sipariş", font=FONT_TITLE,
                 bg=BG_SIDEBAR, fg=TEXT_H).pack(side="left")
        self._masa_badge = tk.Label(oh, text="Masa 1", font=FONT_BADGE,
                                    bg=CAT_LIGHT["drink"], fg=CAT_ACCENT["drink"],
                                    padx=8, pady=2)
        self._masa_badge.pack(side="right")
        self._masa_var.trace_add("write",
            lambda *_: self._masa_badge.config(text=self._masa_var.get()))

        tk.Frame(sb, bg=BORDER, height=1).grid(row=1, column=0, sticky="ew", padx=12)

        # ── Order list
        list_outer = tk.Frame(sb, bg=BG_SIDEBAR)
        list_outer.grid(row=3, column=0, sticky="nsew", padx=8, pady=4)
        list_outer.grid_rowconfigure(0, weight=1)
        list_outer.grid_columnconfigure(0, weight=1)

        canvas2 = tk.Canvas(list_outer, bg=BG_SIDEBAR, bd=0, highlightthickness=0)
        vsb2 = ttk.Scrollbar(list_outer, orient="vertical", command=canvas2.yview)
        canvas2.configure(yscrollcommand=vsb2.set)
        canvas2.grid(row=0, column=0, sticky="nsew")
        vsb2.grid(row=0, column=1, sticky="ns")

        self._order_body = tk.Frame(canvas2, bg=BG_SIDEBAR)
        oid = canvas2.create_window((0, 0), window=self._order_body, anchor="nw")
        canvas2.bind("<Configure>", lambda e: canvas2.itemconfig(oid, width=e.width))
        self._order_body.bind("<Configure>",
                              lambda e: canvas2.configure(scrollregion=canvas2.bbox("all")))

        tk.Frame(sb, bg=BORDER, height=1).grid(row=4, column=0, sticky="ew", padx=12)

        # ── AI Panel
        ai_panel = tk.Frame(sb, bg=INFO_LIGHT, padx=12, pady=8)
        ai_panel.grid(row=5, column=0, sticky="ew", padx=12, pady=6)
        ai_panel.grid_columnconfigure(0, weight=1)

        ai_hdr = tk.Frame(ai_panel, bg=INFO_LIGHT)
        ai_hdr.grid(row=0, column=0, sticky="ew")
        tk.Label(ai_hdr, text="🤖  AI Öneriyor", font=FONT_SMALL_B,
                 bg=INFO_LIGHT, fg=INFO).pack(side="left")
        tk.Label(ai_hdr, text="Geçmişe dayalı",  font=FONT_BADGE,
                 bg=INFO_LIGHT, fg=TEXT_MUTED).pack(side="right")

        self._ai_frame = tk.Frame(ai_panel, bg=INFO_LIGHT)
        self._ai_frame.grid(row=1, column=0, sticky="ew", pady=(4, 0))

        tk.Frame(sb, bg=BORDER, height=1).grid(row=6, column=0, sticky="ew", padx=12)

        # ── Discount
        disc_f = tk.Frame(sb, bg=BG_SIDEBAR, padx=14, pady=6)
        disc_f.grid(row=7, column=0, sticky="ew")
        tk.Label(disc_f, text="🏷  İndirim Kodu", font=FONT_SMALL_B,
                 bg=BG_SIDEBAR, fg=TEXT_B).pack(anchor="w")
        code_row = tk.Frame(disc_f, bg=BG_SIDEBAR)
        code_row.pack(fill="x", pady=(4, 0))
        self._code_var = tk.StringVar()
        tk.Entry(code_row, textvariable=self._code_var, font=FONT_ENTRY,
                 bg=BG_INPUT, fg=TEXT_H, insertbackground=TEXT_H, relief="flat",
                 bd=0, highlightthickness=1, highlightbackground=BORDER_MED,
                 highlightcolor=ACCENT, width=13).pack(side="left", ipady=5)
        tk.Button(code_row, text="Uygula", font=FONT_BTN_SM,
                  bg=ACCENT, fg="white", bd=0, padx=10,
                  activebackground=ACCENT_HOVER, activeforeground="white",
                  cursor="hand2", command=self._apply_discount
                  ).pack(side="left", padx=(6, 0))
        self._disc_lbl = tk.Label(disc_f, text="", font=FONT_SMALL,
                                  bg=BG_SIDEBAR, fg=SUCCESS)
        self._disc_lbl.pack(anchor="w", pady=(2, 0))

        tk.Frame(sb, bg=BORDER, height=1).grid(row=8, column=0, sticky="ew", padx=12)

        # ── Totals
        tot_f = tk.Frame(sb, bg=BG_SIDEBAR, padx=14, pady=8)
        tot_f.grid(row=9, column=0, sticky="ew")
        tot_f.grid_columnconfigure(1, weight=1)

        self._sub_lbl  = self._tot_row(tot_f, 0, "Ara Toplam",   TEXT_SEC)
        self._disc_amt = self._tot_row(tot_f, 1, "İndirim",       DANGER)
        self._kdv_lbl  = self._tot_row(tot_f, 2, "KDV (%8)",      TEXT_SEC)
        tk.Frame(tot_f, bg=BORDER_MED, height=1).grid(row=3, column=0, columnspan=2,
                                                       sticky="ew", pady=4)
        self._total_lbl= self._tot_row(tot_f, 4, "GENEL TOPLAM", ACCENT, big=True)

        # ── Buttons
        btn_f = tk.Frame(sb, bg=BG_SIDEBAR, padx=12, pady=8)
        btn_f.grid(row=10, column=0, sticky="ew")
        btn_f.grid_columnconfigure(0, weight=1)
        btn_f.grid_columnconfigure(1, weight=1)

        tk.Button(btn_f, text="✓  SİPARİŞ VER", font=FONT_BTN,
                  bg=SUCCESS, fg="white", bd=0, pady=13,
                  activebackground="#166534", activeforeground="white",
                  cursor="hand2", command=self._place_order
                  ).grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 6))

        tk.Button(btn_f, text="🧾  Geçmiş", font=FONT_BTN_SM,
                  bg=BG_CARD2, fg=TEXT_B, bd=0, pady=8,
                  activebackground=INFO_LIGHT, activeforeground=INFO,
                  cursor="hand2", command=self._show_history
                  ).grid(row=1, column=0, sticky="ew", padx=(0, 4))

        tk.Button(btn_f, text="📊  Analiz", font=FONT_BTN_SM,
                  bg=BG_CARD2, fg=TEXT_B, bd=0, pady=8,
                  activebackground=WARNING_LIGHT, activeforeground=WARNING,
                  cursor="hand2", command=self._show_analytics
                  ).grid(row=1, column=1, sticky="ew", padx=(4, 0))

        tk.Button(btn_f, text="↺  Sıfırla", font=FONT_BTN_SM,
                  bg=DANGER_LIGHT, fg=DANGER, bd=0, pady=8,
                  activebackground="#FCA5A5", activeforeground=DANGER,
                  cursor="hand2", command=self._reset
                  ).grid(row=2, column=0, columnspan=2, sticky="ew", pady=(6, 0))

    def _tot_row(self, parent, row, label, color, big=False):
        font_lbl  = FONT_ITEM_B if big else FONT_SMALL
        font_val  = FONT_TOTAL  if big else FONT_PRICE
        tk.Label(parent, text=label, font=font_lbl,
                 bg=BG_SIDEBAR, fg=TEXT_B if big else TEXT_SEC
                 ).grid(row=row, column=0, sticky="w", pady=2)
        lbl = tk.Label(parent, text="₺0", font=font_val,
                       bg=BG_SIDEBAR, fg=color, anchor="e")
        lbl.grid(row=row, column=1, sticky="e", pady=2)
        return lbl

    # ── Status bar ────────────────────────────────────────────────────────────
    def _build_statusbar(self):
        bar = tk.Frame(self, bg=BG_CARD2, pady=5)
        bar.grid(row=2, column=0, columnspan=2, sticky="ew")
        self._status_lbl = tk.Label(bar, text="Hazır — ürün seçmeye başlayın.",
                                    font=FONT_SMALL, bg=BG_CARD2, fg=TEXT_MUTED)
        self._status_lbl.pack(side="left", padx=16)
        self._item_count_lbl = tk.Label(bar, text="",
                                        font=FONT_SMALL_B, bg=BG_CARD2, fg=ACCENT)
        self._item_count_lbl.pack(side="right", padx=16)

    # ══════════════════════════════════════════════════════════════════════════
    #  LIVE UPDATE
    # ══════════════════════════════════════════════════════════════════════════
    def _get_active(self):
        return [(n, q) for n, q in (r.get_order() for r in self._rows.values()) if q > 0]

    def _live_update(self):
        orders   = self._get_active()
        subtotal = sum(MENU[n]["price"] * q for n, q in orders)
        disc_amt = round(subtotal * self._discount_pct / 100)
        after    = subtotal - disc_amt
        kdv      = round(after * 0.08)
        total    = after + kdv

        # ── order list
        for w in self._order_body.winfo_children():
            w.destroy()
        if not orders:
            tk.Label(self._order_body, text="Henüz ürün seçilmedi.",
                     font=FONT_SMALL, bg=BG_SIDEBAR, fg=TEXT_MUTED,
                     pady=12).pack()
        for name, qty in orders:
            info  = MENU[name]
            cat   = info["cat"]
            row_f = tk.Frame(self._order_body, bg=BG_CARD2, pady=5)
            row_f.pack(fill="x", padx=6, pady=2)

            tk.Frame(row_f, bg=CAT_ACCENT[cat], width=3).pack(side="left", fill="y")
            tk.Label(row_f, text=f"{info['emoji']}  {name}",
                     font=FONT_SMALL, bg=BG_CARD2, fg=TEXT_H,
                     anchor="w").pack(side="left", padx=(6, 0))
            tk.Label(row_f, text=f"×{qty}  ₺{info['price']*qty:,}",
                     font=FONT_PRICE, bg=BG_CARD2, fg=CAT_ACCENT[cat],
                     anchor="e").pack(side="right", padx=8)

        # ── totals
        self._sub_lbl.config(text=f"₺{subtotal:,}")
        self._disc_amt.config(text=f"−₺{disc_amt:,}" if disc_amt else "₺0")
        self._kdv_lbl.config(text=f"₺{kdv:,}")
        self._total_lbl.config(text=f"₺{total:,}")

        # ── AI suggestions
        for w in self._ai_frame.winfo_children():
            w.destroy()
        suggestions = self._ai.suggest(orders, top_n=3)
        if suggestions:
            for sname, semoji, conf_pct, reason in suggestions:
                sf = tk.Frame(self._ai_frame, bg=INFO_LIGHT)
                sf.pack(fill="x", pady=2)
                left = tk.Frame(sf, bg=INFO_LIGHT)
                left.pack(side="left", fill="x", expand=True)
                tk.Label(left, text=f"{semoji}  {sname}",
                         font=FONT_SMALL_B, bg=INFO_LIGHT, fg=TEXT_H
                         ).pack(anchor="w")
                tk.Label(left, text=reason,
                         font=FONT_AI, bg=INFO_LIGHT, fg=TEXT_SEC
                         ).pack(anchor="w")
                conf_badge = tk.Frame(sf, bg=INFO_LIGHT)
                conf_badge.pack(side="right", padx=(0, 4))
                tk.Label(conf_badge, text=f"%{conf_pct}",
                         font=FONT_BADGE, bg=INFO, fg="white",
                         padx=5, pady=2).pack()
        else:
            tk.Label(self._ai_frame,
                     text="Ürün seçilince öneri gelir…",
                     font=FONT_SMALL, bg=INFO_LIGHT, fg=TEXT_MUTED).pack(anchor="w")

        # ── status bar
        n_items = sum(q for _, q in orders)
        if n_items:
            self._status_lbl.config(
                text=f"✓  {self._masa_var.get()}  ·  {len(orders)} çeşit  ·  {n_items} adet",
                fg=SUCCESS)
            self._item_count_lbl.config(text=f"Toplam  ₺{total:,}")
        else:
            self._status_lbl.config(text="Hazır — ürün seçmeye başlayın.", fg=TEXT_MUTED)
            self._item_count_lbl.config(text="")

    # ══════════════════════════════════════════════════════════════════════════
    #  ACTIONS
    # ══════════════════════════════════════════════════════════════════════════
    def _apply_discount(self):
        code = self._code_var.get().strip().upper()
        if code in DISCOUNT_CODES:
            self._discount_pct = DISCOUNT_CODES[code]
            self._disc_lbl.config(text=f"✓  %{self._discount_pct} indirim uygulandı!", fg=SUCCESS)
        else:
            self._discount_pct = 0
            self._disc_lbl.config(text="✗  Geçersiz kod.", fg=DANGER)
        self._live_update()

    def _place_order(self):
        orders = self._get_active()
        if not orders:
            messagebox.showwarning("Boş Sipariş", "Lütfen en az bir ürün seçin.")
            return
        subtotal = sum(MENU[n]["price"] * q for n, q in orders)
        disc_amt = round(subtotal * self._discount_pct / 100)
        total    = round((subtotal - disc_amt) * 1.08)
        ts       = datetime.datetime.now().strftime("%H:%M  %d.%m.%Y")
        masa     = self._masa_var.get()
        self._order_history.append((ts, masa, list(orders), total, self._discount_pct))

        lines = "\n".join(
            f"  {MENU[n]['emoji']}  {n:<22} ×{q}   ₺{MENU[n]['price']*q:>6,}"
            for n, q in orders)
        disc_line = f"  İndirim (%{self._discount_pct})            −₺{disc_amt:>5,}\n" \
                    if disc_amt else ""
        msg = (f"Masa : {masa}\nSaat : {ts}\n"
               f"{'─'*44}\n{lines}\n{'─'*44}\n"
               f"{disc_line}"
               f"  KDV (%8)                      ₺{round((subtotal-disc_amt)*0.08):>5,}\n"
               f"{'─'*44}\n  TOPLAM                         ₺{total:>5,}")
        messagebox.showinfo("✓  Sipariş Verildi", msg)
        self._reset()

    def _show_history(self):
        if not self._order_history:
            messagebox.showinfo("Geçmiş", "Henüz tamamlanmış sipariş yok.")
            return
        win = tk.Toplevel(self)
        win.title("Sipariş Geçmişi")
        win.geometry("560x520")
        win.configure(bg=BG_MAIN)
        win.grab_set()

        tk.Label(win, text="🧾  Sipariş Geçmişi", font=FONT_TITLE,
                 bg=BG_MAIN, fg=TEXT_H, pady=12).pack()
        tk.Label(win, text=f"{len(self._order_history)} sipariş tamamlandı",
                 font=FONT_SMALL, bg=BG_MAIN, fg=TEXT_MUTED).pack()
        tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=16, pady=4)

        canvas = tk.Canvas(win, bg=BG_MAIN, bd=0, highlightthickness=0)
        vsb = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True, padx=12)

        body = tk.Frame(canvas, bg=BG_MAIN)
        bid  = canvas.create_window((0, 0), window=body, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(bid, width=e.width))
        body.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        grand = sum(t for *_, t, _ in self._order_history)
        for ts, masa, items, total, disc in reversed(self._order_history):
            card = tk.Frame(body, bg=BG_CARD, pady=8, padx=12,
                            highlightthickness=1, highlightbackground=BORDER)
            card.pack(fill="x", pady=4, padx=4)
            h = tk.Frame(card, bg=BG_CARD)
            h.pack(fill="x")
            tk.Label(h, text=f"📍 {masa}", font=FONT_SMALL_B,
                     bg=BG_CARD, fg=CAT_ACCENT["drink"]).pack(side="left")
            tk.Label(h, text=ts, font=FONT_MONO,
                     bg=BG_CARD, fg=TEXT_MUTED).pack(side="right")
            for n, q in items:
                tk.Label(card, text=f"  {MENU[n]['emoji']}  {n}  ×{q}",
                         font=FONT_SMALL, bg=BG_CARD, fg=TEXT_B).pack(anchor="w")
            foot = tk.Frame(card, bg=BG_CARD)
            foot.pack(fill="x", pady=(4, 0))
            if disc:
                tk.Label(foot, text=f"İndirim: %{disc}", font=FONT_BADGE,
                         bg=SUCCESS_LIGHT, fg=SUCCESS, padx=4).pack(side="left")
            tk.Label(foot, text=f"₺{total:,}", font=FONT_PRICE,
                     bg=BG_CARD, fg=ACCENT).pack(side="right")

        tk.Label(body, text=f"Oturum Cirosu:  ₺{grand:,}",
                 font=FONT_TITLE, bg=BG_MAIN, fg=SUCCESS, pady=8).pack()

    def _show_analytics(self):
        win = tk.Toplevel(self)
        win.title("AI Analiz Paneli")
        win.geometry("500x560")
        win.configure(bg=BG_MAIN)
        win.grab_set()

        tk.Label(win, text="📊  AI Analiz Paneli", font=FONT_TITLE,
                 bg=BG_MAIN, fg=TEXT_H, pady=12).pack()
        tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=16)

        # Top items
        top_frame = tk.Frame(win, bg=BG_CARD, padx=16, pady=12)
        top_frame.pack(fill="x", padx=16, pady=10)
        tk.Label(top_frame, text="🏆  En Çok Sipariş Edilen Ürünler",
                 font=FONT_SECTION, bg=BG_CARD, fg=TEXT_H).pack(anchor="w", pady=(0, 8))

        top_items = self._ai.top_items(8)
        max_cnt   = top_items[0][1] if top_items else 1
        for name, cnt in top_items:
            cat = MENU[name]["cat"]
            row = tk.Frame(top_frame, bg=BG_CARD)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=f"{MENU[name]['emoji']}  {name}",
                     font=FONT_SMALL, bg=BG_CARD, fg=TEXT_B, width=22, anchor="w"
                     ).pack(side="left")
            bar_f = tk.Frame(row, bg=BG_CARD)
            bar_f.pack(side="left", fill="x", expand=True)
            bar = MiniBar(bar_f, color=CAT_ACCENT[cat])
            bar.pack(fill="x", pady=4)
            bar.set(cnt / max_cnt)
            tk.Label(row, text=str(cnt), font=FONT_BADGE,
                     bg=BG_CARD, fg=TEXT_MUTED).pack(side="right", padx=(4, 0))

        # Category share
        cat_frame = tk.Frame(win, bg=BG_CARD, padx=16, pady=12)
        cat_frame.pack(fill="x", padx=16, pady=(0, 10))
        tk.Label(cat_frame, text="📂  Kategori Dağılımı",
                 font=FONT_SECTION, bg=BG_CARD, fg=TEXT_H).pack(anchor="w", pady=(0, 8))
        stats = self._ai.category_stats()
        for cat, pct in sorted(stats.items(), key=lambda x: -x[1]):
            label, _ = CATEGORIES.get(cat, (cat, cat))
            row = tk.Frame(cat_frame, bg=BG_CARD)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=label, font=FONT_SMALL, bg=BG_CARD,
                     fg=TEXT_B, width=18, anchor="w").pack(side="left")
            bar_f = tk.Frame(row, bg=BG_CARD)
            bar_f.pack(side="left", fill="x", expand=True)
            bar = MiniBar(bar_f, color=CAT_ACCENT[cat])
            bar.pack(fill="x", pady=4)
            bar.set(pct / 100)
            tk.Label(row, text=f"%{pct}", font=FONT_BADGE,
                     bg=CAT_LIGHT[cat], fg=CAT_ACCENT[cat],
                     padx=4).pack(side="right")

        # AI model info
        info_f = tk.Frame(win, bg=INFO_LIGHT, padx=14, pady=8)
        info_f.pack(fill="x", padx=16, pady=(0, 10))
        tk.Label(info_f, text="🤖  Model Bilgisi", font=FONT_SMALL_B,
                 bg=INFO_LIGHT, fg=INFO).pack(anchor="w")
        total_pairs = sum(self._ai.pair_counts.values()) // 2
        tk.Label(info_f,
                 text=(f"Eğitim siparişi: {len(GECMIS)}  ·  "
                       f"Benzersiz ürün: {len(self._ai.item_counts)}  ·  "
                       f"Çift ilişki: {total_pairs}"),
                 font=FONT_MONO, bg=INFO_LIGHT, fg=TEXT_SEC).pack(anchor="w")
        tk.Label(info_f,
                 text="Algoritma: İtem-bazlı co-occurrence + confidence scoring",
                 font=FONT_MONO, bg=INFO_LIGHT, fg=TEXT_MUTED).pack(anchor="w")

    def _reset(self):
        for row in self._rows.values():
            row.reset()
        self._discount_pct = 0
        self._code_var.set("")
        self._disc_lbl.config(text="")
        self._live_update()


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = RestaurantApp()
    app.mainloop()