#!/usr/bin/env python3
"""
Hypothekenrechner / Mortgage Calculator
Requires: matplotlib (pip install matplotlib)
"""

import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.ticker as mticker
import json
import os

# ── Farben / Colors ───────────────────────────────────────────────────────────
C_BG     = "#1D3557"
C_PANEL  = "#F0F4F8"
C_WHITE  = "#FFFFFF"
C_GREEN  = "#1D9E75"
C_RED    = "#D85A30"
C_GRAY   = "#888780"
C_WARN   = "#E74C3C"
C_WARNBG = "#FDE8E8"
C_TEXT   = "#1A1A2E"
C_MUTED  = "#666677"
C_ACCENT = "#378ADD"
C_MARINE = "#1565C0"

SETTINGS_FILE = "hypothekenrechner_settings.json"

DEFAULTS = {
    "kaufpreis":      100000,
    "eigenkapital":   20000,
    "nebenkosten":    7.0,
    "zinssatz":       3.0,
    "jahre":          10,
    "rate":           1500,
    "zielrest":       0,
    "guthabenzins":   1.0,
    "immosteigerung": 1.0,
}

T = {
    "de": {
        "title":           "Hypothekenrechner + Sparvergleich",
        "subtitle":        "Annuitätendarlehen + Sparvergleich",
        "inputs":          "Eingaben  (Tab / Pfeiltasten)",
        "hypothek":        "-- Hypothek --",
        "sparvergleich":   "-- Sparvergleich --",
        "kaufpreis":       "Kaufpreis",
        "eigenkapital":    "Eigenkapital",
        "nebenkosten":     "Nebenkosten",
        "zinssatz":        "Zinssatz (eff. p.a.)",
        "jahre":           "Zinsbindung",
        "rate":            "Monatsrate",
        "zielrest":        "Zielrestschuld",
        "guthabenzins":    "Guthabenzins (p.a.)",
        "immosteigerung":  "Immo-Wertsteigerung p.a.",
        "warn_rate":       "Warnung: Rate deckt nicht einmal die Zinsen!",
        "warn_ek":         "Warnung: Eigenkapital < Nebenkosten (Vollfinanzierung!)",
        "c_darlehen":      "Darlehensbetrag",
        "c_restschuld":    "Restschuld",
        "c_effgetilgt":    "Effektiv getilgt",
        "c_gezinsen":      "Gezahlte Zinsen",
        "c_sparguthaben":  "Sparguthaben nach Lz.",
        "c_vorteil":       "Vorteil Sparer (+) / Käufer (-)",
        "c_immozuwachs":   "Immo-Wertzuwachs\n(absolut)",
        "c_immowert":      "Immowert nach Lz.",
        "c_immonetto":     "Immo-Nettoverm.\n(Immowert - Restschuld - Zinsen - NK)",
        "banner_vorteil":  "Vorteil:",
        "banner_mind":     "  |  Mindestrate (Ziel):",
        "vorteil_sparer":  "Sparer",
        "vorteil_immo":    "Immokauf",
        "vorteil_info_s":  "(Sparguthaben {spar} > Immo-Netto {immo})",
        "vorteil_info_i":  "(Immo-Netto {immo} > Sparguthaben {spar})",
        "summary":         "Kaufpreis {kp}  |  NK {nk} ({nkp})  |  EK {ek}  |  Darlehen {d}  |  eff. getilgt {et}",
        "leg_tilgung":     "Tilgung",
        "leg_zinsen":      "Zinsen (Balken)",
        "leg_rest_man":    "Restschuld (manuell)",
        "leg_rest_ziel":   "Restschuld (Ziel)",
        "leg_spar":        "Sparguthaben",
        "leg_kum":         "Kum. Zinsen",
        "leg_immo":        "Immowert",
        "tt_zinsen":       "Zinsen:",
        "tt_tilgung":      "Tilgung:",
        "tt_gesamt":       "Gesamt:",
        "jahre_unit":      "Jahre",
        "lang_btn":        "Sprache",
        "tip_darlehen":    "Darlehensbetrag\n\nKaufpreis + Nebenkosten - Eigenkapital.\nDiesen Betrag leiht dir die Bank.",
        "tip_restschuld":  "Restschuld\n\nNoch offener Kreditbetrag nach der\ngewählten Laufzeit. Muss danach neu\nfinanziert werden (Anschlussfinanzierung).",
        "tip_effgetilgt":  "Effektiv getilgt\n\nDarlehensbetrag minus Restschuld.\nDas ist dein aufgebautes Eigenkapital\nals Käufer nach der Laufzeit.",
        "tip_gezinsen":    "Gezahlte Zinsen\n\nGesamte Zinszahlungen an die Bank\nüber die gesamte Laufzeit.\nDieses Geld ist unwiederbringlich weg.",
        "tip_sparguthaben":"Sparguthaben\n\nAngespartes Kapital wenn du statt\nder Kreditrate monatlich sparst.\nMit Zinseszins-Effekt (Guthabenzins).",
        "tip_vorteil":     "Vorteil Sparer / Käufer\n\nVergleich: Sparguthaben minus\nImmo-Nettovermögen.\n+ = Sparen ist besser\n- = Immokauf ist besser",
        "tip_immozuwachs": "Immo-Wertzuwachs\n\nAbsoluter Wertzuwachs der Immobilie\ndurch Preissteigerung über die Laufzeit.\n(Immowert Ende - Kaufpreis)",
        "tip_immowert":    "Immowert nach Laufzeit\n\nGeschätzter Marktwert der Immobilie\nnach der Laufzeit basierend auf der\ngewählten Wertsteigerung p.a.",
        "tip_immonetto":   "Immo-Nettovermögen\n\nImmowert\n- Restschuld (noch offen)\n- Gezahlte Zinsen (verbrannt)\n- Nebenkosten (verbrannt)\n= Echter Vermögenswert des Käufers",
    },
    "en": {
        "title":           "Mortgage Calculator + Savings Comparison",
        "subtitle":        "Annuity Loan + Savings Comparison",
        "inputs":          "Inputs  (Tab / Arrow Keys)",
        "hypothek":        "-- Mortgage --",
        "sparvergleich":   "-- Savings Comparison --",
        "kaufpreis":       "Purchase Price",
        "eigenkapital":    "Equity",
        "nebenkosten":     "Ancillary Costs",
        "zinssatz":        "Interest Rate (eff. p.a.)",
        "jahre":           "Fixed Rate Period",
        "rate":            "Monthly Payment",
        "zielrest":        "Target Residual Debt",
        "guthabenzins":    "Savings Interest (p.a.)",
        "immosteigerung":  "Property Appreciation p.a.",
        "warn_rate":       "Warning: Payment does not cover interest!",
        "warn_ek":         "Warning: Equity < Ancillary Costs (Full Financing!)",
        "c_darlehen":      "Loan Amount",
        "c_restschuld":    "Residual Debt",
        "c_effgetilgt":    "Effectively Repaid",
        "c_gezinsen":      "Interest Paid",
        "c_sparguthaben":  "Savings Balance",
        "c_vorteil":       "Advantage Saver (+) / Buyer (-)",
        "c_immozuwachs":   "Property Value Gain\n(absolute)",
        "c_immowert":      "Property Value",
        "c_immonetto":     "Net Property Value\n(Value - Residual - Interest - Costs)",
        "banner_vorteil":  "Advantage:",
        "banner_mind":     "  |  Minimum Payment (Target):",
        "vorteil_sparer":  "Saver",
        "vorteil_immo":    "Property",
        "vorteil_info_s":  "(Savings {spar} > Net Property {immo})",
        "vorteil_info_i":  "(Net Property {immo} > Savings {spar})",
        "summary":         "Price {kp}  |  Costs {nk} ({nkp})  |  Equity {ek}  |  Loan {d}  |  Repaid {et}",
        "leg_tilgung":     "Repayment",
        "leg_zinsen":      "Interest (bars)",
        "leg_rest_man":    "Residual Debt (actual)",
        "leg_rest_ziel":   "Residual Debt (target)",
        "leg_spar":        "Savings",
        "leg_kum":         "Cum. Interest",
        "leg_immo":        "Property Value",
        "tt_zinsen":       "Interest:",
        "tt_tilgung":      "Repayment:",
        "tt_gesamt":       "Total:",
        "jahre_unit":      "Years",
        "lang_btn":        "Language",
        "tip_darlehen":    "Loan Amount\n\nPurchase price + ancillary costs - equity.\nThis is the amount borrowed from the bank.",
        "tip_restschuld":  "Residual Debt\n\nOutstanding loan balance after the\nselected period. Requires refinancing\n(follow-up financing) afterwards.",
        "tip_effgetilgt":  "Effectively Repaid\n\nLoan amount minus residual debt.\nThis is your built-up equity\nas a buyer after the period.",
        "tip_gezinsen":    "Interest Paid\n\nTotal interest payments to the bank\nover the entire period.\nThis money is gone for good.",
        "tip_sparguthaben":"Savings Balance\n\nAccumulated capital if you save\nthe monthly payment instead of taking\na loan. Includes compound interest.",
        "tip_vorteil":     "Advantage Saver / Buyer\n\nComparison: Savings balance minus\nnet property value.\n+ = Saving is better\n- = Buying is better",
        "tip_immozuwachs": "Property Value Gain\n\nAbsolute increase in property value\ndue to price appreciation over the period.\n(Final value - Purchase price)",
        "tip_immowert":    "Property Value\n\nEstimated market value of the property\nafter the period based on the selected\nappreciation rate p.a.",
        "tip_immonetto":   "Net Property Value\n\nProperty value\n- Residual debt (still owed)\n- Interest paid (gone)\n- Ancillary costs (gone)\n= True asset value for the buyer",
    }
}


# ── Berechnungen ──────────────────────────────────────────────────────────────
def calc_mindestrate(darlehen, zins_pa, jahre, ziel_rest):
    r = zins_pa / 100 / 12
    n = jahre * 12
    if darlehen <= 0:
        return 0.0
    if r == 0:
        return (darlehen - ziel_rest) / n if n > 0 else 0.0
    return max((darlehen * r - ziel_rest * r * (1+r)**(-n)) / (1-(1+r)**(-n)), 0.0)

def calc_amortization(darlehen, rate, zins_pa, jahre):
    r = zins_pa / 100 / 12
    schuld = darlehen
    labels, tilg_arr, zins_arr, rest_arr = [], [], [], []
    total_zinsen = 0.0
    for j in range(1, jahre+1):
        jz, jt = 0.0, 0.0
        for _ in range(12):
            if schuld <= 0:
                break
            za = schuld * r
            ta = min(max(rate - za, 0), schuld)
            schuld -= ta
            jz += za
            jt += ta
        total_zinsen += jz
        labels.append(f"Y{j}" if False else f"J{j}")
        tilg_arr.append(round(jt))
        zins_arr.append(round(jz))
        rest_arr.append(round(max(schuld, 0)))
    return labels, tilg_arr, zins_arr, rest_arr, total_zinsen, max(schuld, 0)

def calc_amortization_lang(darlehen, rate, zins_pa, jahre, lang):
    r = zins_pa / 100 / 12
    schuld = darlehen
    labels, tilg_arr, zins_arr, rest_arr = [], [], [], []
    total_zinsen = 0.0
    prefix = "Y" if lang == "en" else "J"
    for j in range(1, jahre+1):
        jz, jt = 0.0, 0.0
        for _ in range(12):
            if schuld <= 0:
                break
            za = schuld * r
            ta = min(max(rate - za, 0), schuld)
            schuld -= ta
            jz += za
            jt += ta
        total_zinsen += jz
        labels.append(f"{prefix}{j}")
        tilg_arr.append(round(jt))
        zins_arr.append(round(jz))
        rest_arr.append(round(max(schuld, 0)))
    return labels, tilg_arr, zins_arr, rest_arr, total_zinsen, max(schuld, 0)

def calc_rest_verlauf(darlehen, rate, zins_pa, jahre):
    r = zins_pa / 100 / 12
    schuld = darlehen
    result = []
    for _ in range(jahre):
        for _ in range(12):
            if schuld <= 0:
                break
            za = schuld * r
            ta = min(max(rate - za, 0), schuld)
            schuld -= ta
        result.append(round(max(schuld, 0)))
    return result

def calc_sparguthaben(rate, guthabenzins_pa, jahre):
    r = guthabenzins_pa / 100 / 12
    guthaben = 0.0
    result = []
    for _ in range(jahre):
        for _ in range(12):
            guthaben += rate
            guthaben *= (1 + r)
        result.append(round(guthaben))
    return result

def fmt_eur(v):
    return f"{round(v):,.0f} EUR".replace(",", ".")

def fmt_pct(v):
    return f"{v:.1f} %".replace(".", ",")

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
            settings = {k: data.get(k, DEFAULTS[k]) for k in DEFAULTS}
            settings["language"] = data.get("language", None)
            return settings
        except Exception:
            pass
    return None   # signals: first run

def save_settings(vals):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(vals, f, indent=2)
    except Exception:
        pass


# ── Sprachauswahl-Dialog ──────────────────────────────────────────────────────
class LanguageDialog(tk.Tk):
    def __init__(self):
        super().__init__()
        self.chosen = None
        self.title("Language / Sprache")
        self.configure(bg=C_BG)
        self.resizable(False, False)
        self.geometry("340x180")
        self._center()

        tk.Label(self, text="Please choose your language",
                 bg=C_BG, fg=C_WHITE, font=("Arial", 12)).pack(pady=(24, 4))
        tk.Label(self, text="Bitte Sprache wählen",
                 bg=C_BG, fg="#90CAF9", font=("Arial", 10)).pack(pady=(0, 20))

        btn_frame = tk.Frame(self, bg=C_BG)
        btn_frame.pack()

        tk.Button(btn_frame, text="English", width=12, height=2,
                  bg=C_MARINE, fg=C_WHITE, font=("Arial", 11, "bold"),
                  relief="flat", cursor="hand2",
                  command=lambda: self._pick("en")).pack(side="left", padx=12)

        tk.Button(btn_frame, text="Deutsch", width=12, height=2,
                  bg=C_GREEN, fg=C_WHITE, font=("Arial", 11, "bold"),
                  relief="flat", cursor="hand2",
                  command=lambda: self._pick("de")).pack(side="left", padx=12)

        self.protocol("WM_DELETE_WINDOW", lambda: self._pick("en"))

    def _center(self):
        self.update_idletasks()
        w, h = 340, 180
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _pick(self, lang):
        self.chosen = lang
        self.destroy()


# ── Hauptfenster ──────────────────────────────────────────────────────────────
class HypoRechner(tk.Tk):
    def __init__(self, settings, lang):
        super().__init__()
        self.lang     = lang
        self._t       = T[lang]
        self.vars     = {}
        self._sliders = []
        self._settings       = settings
        self._chart_tilg     = []
        self._chart_zins     = []
        self._chart_labels   = []
        self._tooltip_win    = None
        self.title(self._t["title"])
        self.configure(bg=C_BG)
        self.resizable(True, True)
        self.minsize(1200, 750)
        self.geometry("1300x800")
        self._center()
        self._build_ui()
        self._update()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _center(self):
        self.update_idletasks()
        w, h = 1300, 800
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"1300x800+{(sw-w)//2}+{(sh-h)//2}")

    def _on_close(self):
        vals = {k: self._get(k) for k in DEFAULTS}
        vals["language"] = self.lang
        save_settings(vals)
        self.destroy()

    def _make_card(self, parent, key, title, fg, row):
        tip_key = f"tip_{key}"
        tip_text = self._t.get(tip_key, "")
        f = tk.Frame(parent, bg=C_WHITE, bd=0, padx=10, pady=7)
        f.grid(row=row, column=0, sticky="nsew",
               pady=(0 if row == 0 else 5, 0))
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        # "?" hint if tooltip available
        top_row = tk.Frame(f, bg=C_WHITE)
        top_row.pack(fill="x")
        tk.Label(top_row, text=title, bg=C_WHITE, fg=C_MUTED,
                 font=("Arial", 8), wraplength=160, justify="left").pack(side="left")
        if tip_text:
            hint = tk.Label(top_row, text=" ?", bg=C_WHITE, fg=C_ACCENT,
                            font=("Arial", 8, "bold"), cursor="question_arrow")
            hint.pack(side="right")
            self._bind_card_tooltip(hint, tip_text)
            self._bind_card_tooltip(f, tip_text)
        v = tk.Label(f, text="-", bg=C_WHITE, fg=fg, font=("Arial", 12, "bold"))
        v.pack(anchor="w")
        self.cards[key] = v

    def _bind_card_tooltip(self, widget, text):
        tip_win = [None]

        def show(event):
            if tip_win[0]:
                return
            tw = tk.Toplevel(self)
            tw.wm_overrideredirect(True)
            tw.attributes("-topmost", True)
            tk.Label(tw, text=text, justify="left", bg="#1A1A2E", fg=C_WHITE,
                     font=("Arial", 9), padx=10, pady=8, relief="flat").pack()
            x = widget.winfo_rootx() + 20
            y = widget.winfo_rooty() + widget.winfo_height() + 4
            tw.wm_geometry(f"+{x}+{y}")
            tip_win[0] = tw

        def hide(event):
            if tip_win[0]:
                tip_win[0].destroy()
                tip_win[0] = None

        widget.bind("<Enter>", show)
        widget.bind("<Leave>", hide)

    def _build_ui(self):
        t = self._t

        # Header
        hdr = tk.Frame(self, bg=C_BG, pady=10)
        hdr.pack(fill="x", padx=16, pady=(12, 0))
        tk.Label(hdr, text=t["title"], bg=C_BG, fg=C_WHITE,
                 font=("Arial", 16, "bold")).pack(side="left")
        tk.Label(hdr, text=t["subtitle"], bg=C_BG, fg="#90CAF9",
                 font=("Arial", 10)).pack(side="left", padx=(12, 0), pady=(4, 0))

        main = tk.Frame(self, bg=C_BG)
        main.pack(fill="both", expand=True, padx=16, pady=10)

        # ── Linke Spalte: Slider ───────────────────────────────────────────────
        left = tk.Frame(main, bg=C_PANEL, bd=0, padx=18, pady=14)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)
        left.configure(width=380)

        tk.Label(left, text=t["inputs"], bg=C_PANEL, fg=C_BG,
                 font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 6))
        tk.Label(left, text=t["hypothek"], bg=C_PANEL, fg=C_MUTED,
                 font=("Arial", 9)).pack(anchor="w", pady=(4, 2))

        for key, mn, mx, step, unit in [
            ("kaufpreis",    10000,  3000000, 5000, "EUR"),
            ("eigenkapital", 0,      400000,  1000, "EUR"),
            ("nebenkosten",  0,      20,      0.5,  "%"),
            ("zinssatz",     0.1,    20.0,    0.1,  "%"),
            ("jahre",        1,      30,      1,    t["jahre_unit"]),
            ("rate",         200,    10000,   50,   "EUR"),
            ("zielrest",     0,      100,     1,    "%"),
        ]:
            self._make_slider(left, key, t[key], mn, mx, step, unit)

        tk.Label(left, text=t["sparvergleich"], bg=C_PANEL, fg=C_MARINE,
                 font=("Arial", 9, "bold")).pack(anchor="w", pady=(10, 2))
        self._make_slider(left, "guthabenzins",   t["guthabenzins"],   0.0, 8.0,  0.1, "%")
        self._make_slider(left, "immosteigerung", t["immosteigerung"], 0.0, 10.0, 0.1, "%")

        self.warn_frame = tk.Frame(left, bg=C_PANEL)
        self.warn_frame.pack(fill="x", pady=(10, 0))
        self.warn_rate_lbl = tk.Label(self.warn_frame, text="", bg=C_WARNBG, fg=C_WARN,
                                       font=("Arial", 9, "bold"), wraplength=320,
                                       justify="left", padx=8, pady=4)
        self.warn_ek_lbl   = tk.Label(self.warn_frame, text="", bg="#FFF8E1", fg="#E65100",
                                       font=("Arial", 9, "bold"), wraplength=320,
                                       justify="left", padx=8, pady=4)

        # ── Rechte Spalte ──────────────────────────────────────────────────────
        right = tk.Frame(main, bg=C_BG)
        right.pack(side="left", fill="both", expand=True)

        # 3 Spalten je 3 Karten
        cards_frame = tk.Frame(right, bg=C_BG)
        cards_frame.pack(fill="x", pady=(0, 4))
        self.cards = {}

        col1 = tk.Frame(cards_frame, bg=C_BG)
        col1.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        cards_frame.grid_columnconfigure(0, weight=1)

        col2 = tk.Frame(cards_frame, bg=C_BG)
        col2.grid(row=0, column=1, sticky="nsew", padx=(0, 5))
        cards_frame.grid_columnconfigure(1, weight=1)

        col3 = tk.Frame(cards_frame, bg=C_BG)
        col3.grid(row=0, column=2, sticky="nsew")
        cards_frame.grid_columnconfigure(2, weight=1)

        self._make_card(col1, "darlehen",    t["c_darlehen"],    C_GRAY,   0)
        self._make_card(col1, "restschuld",  t["c_restschuld"],  C_RED,    1)
        self._make_card(col1, "effgetilgt",  t["c_effgetilgt"],  C_GREEN,  2)

        self._make_card(col2, "gezinsen",    t["c_gezinsen"],    C_RED,    0)
        self._make_card(col2, "sparguthaben",t["c_sparguthaben"],C_MARINE, 1)
        self._make_card(col2, "vorteil_karte",t["c_vorteil"],    C_GREEN,  2)

        self._make_card(col3, "immozuwachs", t["c_immozuwachs"], C_ACCENT, 0)
        self._make_card(col3, "immowert",    t["c_immowert"],    C_ACCENT, 1)
        self._make_card(col3, "immonetto",   t["c_immonetto"],   C_ACCENT, 2)

        # Vorteil-Banner
        vframe = tk.Frame(right, bg=C_BG)
        vframe.pack(fill="x", pady=(4, 2))
        tk.Label(vframe, text=t["banner_vorteil"], bg=C_BG, fg="#90CAF9",
                 font=("Arial", 10)).pack(side="left")
        self.lbl_vorteil = tk.Label(vframe, text="-", bg=C_BG, fg=C_GREEN,
                                     font=("Arial", 13, "bold"))
        self.lbl_vorteil.pack(side="left", padx=(8, 0))
        self.lbl_vorteil_info = tk.Label(vframe, text="", bg=C_BG, fg="#90CAF9",
                                          font=("Arial", 9))
        self.lbl_vorteil_info.pack(side="left", padx=(10, 0))
        tk.Label(vframe, text=t["banner_mind"], bg=C_BG, fg="#90CAF9",
                 font=("Arial", 10)).pack(side="left", padx=(20, 0))
        self.lbl_mindestrate = tk.Label(vframe, text="-", bg=C_BG, fg=C_GRAY,
                                         font=("Arial", 13, "bold"))
        self.lbl_mindestrate.pack(side="left", padx=(6, 0))

        self.lbl_summary = tk.Label(right, text="", bg=C_BG, fg="#90CAF9", font=("Arial", 9))
        self.lbl_summary.pack(anchor="w", pady=(0, 4))

        # Chart
        chart_frame = tk.Frame(right, bg=C_WHITE)
        chart_frame.pack(fill="both", expand=True)

        self.fig = Figure(figsize=(7, 4), dpi=96, facecolor=C_WHITE)
        self.ax  = self.fig.add_subplot(111)
        self.fig.tight_layout(pad=2.0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas.mpl_connect("motion_notify_event", self._on_hover)
        self.canvas.mpl_connect("axes_leave_event",    self._on_leave)

        # Legende
        leg = tk.Frame(right, bg=C_BG)
        leg.pack(fill="x", pady=(4, 0))
        for color, key in [
            (C_GREEN,   "leg_tilgung"),
            (C_RED,     "leg_zinsen"),
            (C_GRAY,    "leg_rest_man"),
            (C_ACCENT,  "leg_rest_ziel"),
            (C_MARINE,  "leg_spar"),
            ("#CC0000",  "leg_kum"),
            ("#FF9800",  "leg_immo"),
        ]:
            dot = tk.Frame(leg, bg=color, width=12, height=12)
            dot.pack(side="left", padx=(0, 4))
            tk.Label(leg, text=t[key], bg=C_BG, fg=C_WHITE,
                     font=("Arial", 9)).pack(side="left", padx=(0, 10))

        self._setup_keyboard_nav()

    def _make_slider(self, parent, key, label, mn, mx, step, unit):
        default = self._settings.get(key, DEFAULTS.get(key, mn))
        frame = tk.Frame(parent, bg=C_PANEL, pady=4)
        frame.pack(fill="x")
        top = tk.Frame(frame, bg=C_PANEL)
        top.pack(fill="x")
        tk.Label(top, text=label, bg=C_PANEL, fg=C_TEXT, font=("Arial", 10)).pack(side="left")
        val_lbl = tk.Label(top, text="", bg=C_PANEL, fg=C_BG, font=("Arial", 10, "bold"))
        val_lbl.pack(side="right")

        if key == "eigenkapital":
            pct_var = tk.StringVar(value="0.0")
            pct_entry = tk.Entry(top, textvariable=pct_var, width=6,
                                 font=("Arial", 9), justify="right",
                                 relief="flat", bg="#E0E8F0", fg=C_MARINE)
            pct_entry.pack(side="right", padx=(0, 4))
            tk.Label(top, text="%", bg=C_PANEL, fg=C_MARINE,
                     font=("Arial", 9)).pack(side="right")
            self._ek_pct_var   = pct_var
            self._ek_pct_entry = pct_entry

        var = tk.DoubleVar(value=default)
        sl  = ttk.Scale(frame, from_=mn, to=mx, variable=var,
                        orient="horizontal", takefocus=True)
        sl.pack(fill="x", pady=(2, 0))
        self.vars[key] = (var, val_lbl, unit, step, mn, mx)
        self._sliders.append((key, sl))

        sl.bind("<FocusIn>",  lambda e, s=sl: s.configure(style="Focused.Horizontal.TScale"))
        sl.bind("<FocusOut>", lambda e, s=sl: s.configure(style="Horizontal.TScale"))
        sl.bind("<Button-1>", lambda e, s=sl: s.focus_set())

        def on_change(*_):
            raw = var.get()
            snapped = round(raw / step) * step
            if abs(raw - snapped) > 1e-9:
                var.set(snapped)
            self._update_label(key)
            if key == "eigenkapital":
                self._update_ek_pct()
            self._update()

        var.trace_add("write", on_change)
        self._update_label(key)

        if key == "eigenkapital":
            def on_pct_enter(e):
                self._apply_ek_pct()
            pct_entry.bind("<Return>",   on_pct_enter)
            pct_entry.bind("<FocusOut>", on_pct_enter)
            # Initialwert: 20% des Kaufpreises anzeigen
            kp_default = self._settings.get("kaufpreis", DEFAULTS["kaufpreis"])
            ek_default = self._settings.get("eigenkapital", DEFAULTS["eigenkapital"])
            pct_init = (ek_default / kp_default * 100) if kp_default > 0 else 20.0
            pct_var.set(f"{pct_init:.1f}")

    def _update_ek_pct(self):
        kp  = self._get("kaufpreis")
        ek  = self._get("eigenkapital")
        pct = (ek / kp * 100) if kp > 0 else 0.0
        self._ek_pct_var.set(f"{pct:.1f}")

    def _apply_ek_pct(self):
        try:
            raw = self._ek_pct_var.get().replace(",", ".").strip().rstrip("%")
            pct = max(0.0, min(100.0, float(raw)))
            kp  = self._get("kaufpreis")
            ek  = max(0, min(400000, round(kp * pct / 100 / 1000) * 1000))
            self.vars["eigenkapital"][0].set(ek)
        except ValueError:
            self._update_ek_pct()

    def _setup_keyboard_nav(self):
        ttk.Style().configure("Focused.Horizontal.TScale", troughcolor="#2196F3")
        slider_widgets = [sl for _, sl in self._sliders]
        n = len(slider_widgets)
        for idx, (key, sl) in enumerate(self._sliders):
            var, _, _, step, mn, mx = self.vars[key]

            def make_arrow(v=var, s=step, lo=mn, hi=mx):
                def handler(event):
                    delta = s if event.keysym == "Right" else -s
                    v.set(max(lo, min(hi, round((v.get() + delta) / s) * s)))
                    return "break"
                return handler

            sl.bind("<Left>",      make_arrow())
            sl.bind("<Right>",     make_arrow())
            sl.bind("<Tab>",
                    lambda e, i=idx, w=slider_widgets, t=n: (w[(i+1)%t].focus_set(), "break")[1])
            sl.bind("<Shift-Tab>",
                    lambda e, i=idx, w=slider_widgets, t=n: (w[(i-1)%t].focus_set(), "break")[1])

        if slider_widgets:
            self.after(100, slider_widgets[0].focus_set)

    def _update_label(self, key):
        var, lbl, unit, step, mn, mx = self.vars[key]
        v = round(var.get() / step) * step
        if unit == "EUR":
            lbl.config(text=fmt_eur(v))
        elif unit == "%":
            lbl.config(text=fmt_pct(v))
        else:
            lbl.config(text=f"{int(round(v))} {unit}")

    def _get(self, key):
        var, _, _, step, mn, mx = self.vars[key]
        return round(var.get() / step) * step

    def _on_hover(self, event):
        if event.inaxes != self.ax or not self._chart_labels:
            self._hide_tooltip()
            return
        idx = int(round(event.xdata))
        if idx < 0 or idx >= len(self._chart_labels):
            self._hide_tooltip()
            return
        t = self._t
        tilg  = self._chart_tilg[idx]
        zins  = self._chart_zins[idx]
        label = self._chart_labels[idx]
        text  = (f"{label}\n"
                 f"{t['tt_zinsen']}   {fmt_eur(zins)}\n"
                 f"{t['tt_tilgung']}  {fmt_eur(tilg)}\n"
                 f"{t['tt_gesamt']}   {fmt_eur(zins + tilg)}")
        x_root = self.canvas.get_tk_widget().winfo_rootx() + int(event.x) + 15
        y_root = self.canvas.get_tk_widget().winfo_rooty() + \
                 self.canvas.get_tk_widget().winfo_height() - int(event.y) + 5
        self._show_tooltip(x_root, y_root, text)

    def _on_leave(self, event):
        self._hide_tooltip()

    def _show_tooltip(self, x, y, text):
        if self._tooltip_win:
            self._tooltip_win.destroy()
        tw = tk.Toplevel(self)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.attributes("-topmost", True)
        tk.Label(tw, text=text, justify="left", bg="#1A1A2E", fg=C_WHITE,
                 font=("Courier", 10), padx=10, pady=6, relief="flat").pack()
        self._tooltip_win = tw

    def _hide_tooltip(self):
        if self._tooltip_win:
            self._tooltip_win.destroy()
            self._tooltip_win = None

    def _update(self):
        t = self._t
        kaufpreis      = self._get("kaufpreis")
        ek             = self._get("eigenkapital")
        nk_pct         = self._get("nebenkosten")
        zins           = self._get("zinssatz")
        jahre          = int(self._get("jahre"))
        rate           = self._get("rate")
        ziel_pct       = self._get("zielrest")
        guthabenzins   = self._get("guthabenzins")
        immosteigerung = self._get("immosteigerung")

        self._update_ek_pct()

        nk_eur      = kaufpreis * nk_pct / 100
        darlehen    = max(kaufpreis + nk_eur - ek, 0)
        ziel_rest   = darlehen * ziel_pct / 100
        mindestrate = calc_mindestrate(darlehen, zins, jahre, ziel_rest)

        min_zins = darlehen * (zins / 100 / 12)
        if rate <= min_zins and darlehen > 0:
            self.warn_rate_lbl.config(text=t["warn_rate"])
            self.warn_rate_lbl.pack(fill="x", pady=(0, 3))
        else:
            self.warn_rate_lbl.pack_forget()

        if ek < nk_eur:
            self.warn_ek_lbl.config(text=t["warn_ek"])
            self.warn_ek_lbl.pack(fill="x", pady=(0, 3))
        else:
            self.warn_ek_lbl.pack_forget()

        labels, tilg, zinsen_arr, rest_ist, total_zinsen, restschuld = \
            calc_amortization_lang(darlehen, rate, zins, jahre, self.lang)
        rest_ziel         = calc_rest_verlauf(darlehen, mindestrate, zins, jahre)
        sparguthaben      = calc_sparguthaben(rate, guthabenzins, jahre)
        sparguthaben_null = calc_sparguthaben(rate, 0.0, jahre)

        kum_zinsen = []
        laufend = 0
        for z in zinsen_arr:
            laufend += z
            kum_zinsen.append(laufend)

        immowert_arr = []
        for j in range(1, jahre + 1):
            immowert_arr.append(round(kaufpreis * ((1 + immosteigerung / 100) ** j)))

        effektiv_getilgt = darlehen - restschuld
        immowert_end     = immowert_arr[-1] if immowert_arr else kaufpreis
        immozuwachs      = immowert_end - kaufpreis
        spar_end         = sparguthaben[-1] if sparguthaben else 0
        immo_netto       = immowert_end - restschuld - total_zinsen - nk_eur
        vorteil          = spar_end - immo_netto

        self._chart_tilg   = tilg
        self._chart_zins   = zinsen_arr
        self._chart_labels = labels

        self.cards["darlehen"].config(text=fmt_eur(darlehen))
        self.cards["restschuld"].config(text=fmt_eur(restschuld))
        self.cards["effgetilgt"].config(text=fmt_eur(effektiv_getilgt))
        self.cards["gezinsen"].config(text=fmt_eur(total_zinsen))
        self.cards["sparguthaben"].config(text=fmt_eur(spar_end))
        self.cards["immozuwachs"].config(text=fmt_eur(immozuwachs))
        self.cards["immowert"].config(text=fmt_eur(immowert_end))
        self.cards["immonetto"].config(text=fmt_eur(immo_netto))
        v_color = C_RED if vorteil < 0 else C_GREEN
        self.cards["vorteil_karte"].config(
            text=("+" if vorteil >= 0 else "") + fmt_eur(vorteil),
            fg=v_color)

        self.lbl_mindestrate.config(text=fmt_eur(mindestrate) + " / Mo." if self.lang == "de" else fmt_eur(mindestrate) + " / mo.")

        if vorteil > 0:
            self.lbl_vorteil.config(text=f"+{fmt_eur(vorteil)}  {t['vorteil_sparer']}", fg=C_GREEN)
            self.lbl_vorteil_info.config(
                text=t["vorteil_info_s"].format(spar=fmt_eur(spar_end), immo=fmt_eur(immo_netto)))
        else:
            self.lbl_vorteil.config(text=f"{fmt_eur(vorteil)}  {t['vorteil_immo']}", fg=C_RED)
            self.lbl_vorteil_info.config(
                text=t["vorteil_info_i"].format(immo=fmt_eur(immo_netto), spar=fmt_eur(spar_end)))

        self.lbl_summary.config(text=t["summary"].format(
            kp=fmt_eur(kaufpreis), nk=fmt_eur(nk_eur), nkp=fmt_pct(nk_pct),
            ek=fmt_eur(ek), d=fmt_eur(darlehen), et=fmt_eur(effektiv_getilgt)))

        self.ax.clear()
        x = list(range(len(labels)))

        self.ax.bar(x, tilg,       color=C_GREEN,   alpha=0.85)
        self.ax.bar(x, zinsen_arr, bottom=tilg,      color=C_RED,     alpha=0.85)
        self.ax.plot(x, rest_ist,          color=C_GRAY,    lw=1.8, marker="o", ms=3)
        self.ax.plot(x, rest_ziel,         color=C_ACCENT,  lw=1.8, marker="o", ms=3, ls="--")
        self.ax.plot(x, sparguthaben,      color=C_MARINE,  lw=2.2, marker="D", ms=4, zorder=5)
        self.ax.plot(x, sparguthaben_null, color=C_MARINE,  lw=1.2, ls=":",     alpha=0.4)
        self.ax.plot(x, kum_zinsen,        color="#CC0000", lw=2.0, marker="x", ms=5, zorder=6)
        self.ax.plot(x, immowert_arr,      color="#FF9800", lw=2.0, marker="s", ms=4, zorder=5)

        self.ax.set_xticks(x)
        self.ax.set_xticklabels(labels, fontsize=8, rotation=45 if jahre > 15 else 0)
        self.ax.yaxis.set_major_formatter(
            mticker.FuncFormatter(lambda v, _: f"{int(v):,}".replace(",", ".")))
        self.ax.tick_params(axis="y", labelsize=8)
        self.ax.set_facecolor(C_WHITE)
        self.fig.set_facecolor(C_WHITE)
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["left"].set_color("#CCCCCC")
        self.ax.spines["bottom"].set_color("#CCCCCC")
        self.ax.grid(axis="y", ls="--", alpha=0.4, color="#CCCCCC")
        self.ax.set_ylabel("EUR", fontsize=9, color=C_MUTED)
        self.fig.tight_layout(pad=2.0)
        self.canvas.draw()


# ── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    settings = load_settings()

    if settings is None or settings.get("language") is None:
        # Erster Start: Sprachauswahl
        dlg = LanguageDialog()
        dlg.mainloop()
        lang = dlg.chosen if dlg.chosen else "en"
        settings = dict(DEFAULTS)
        settings["language"] = lang
        save_settings(settings)
    else:
        lang = settings["language"]

    app = HypoRechner(settings, lang)
    app.mainloop()
