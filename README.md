# 🏠 Hypothekenrechner / Mortgage Calculator

Ein interaktiver Hypotheken- und Sparvergleichsrechner mit grafischer Oberfläche.  
An interactive mortgage and savings comparison calculator with a graphical interface.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![License](https://img.shields.io/badge/License-Apache%202.0-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)


<img width="418" height="273" alt="grafik" src="https://github.com/user-attachments/assets/140273c4-166c-40df-bd37-115e36692fd9" />

## 🇩🇪 Deutsche Oberfläche

<img width="1302" height="832" alt="grafik" src="https://github.com/user-attachments/assets/1e5a7900-19fe-4e5f-b555-08797ed4dae8" />

## 🇬🇧 English UI

<img width="1302" height="832" alt="grafik" src="https://github.com/user-attachments/assets/aa84bbfd-9d2f-47ca-8f72-c28adfa4f69d" />



---

## 🇩🇪 Deutsch

### Features
- Annuitätendarlehen-Berechnung mit allen relevanten Parametern
- Sparvergleich: Monatlich sparen vs. Immobilienkauf
- Immobilien-Wertsteigerung einstellbar
- Immo-Nettovermögen: ehrlicher Vergleich inkl. Zinsen und Nebenkosten
- Interaktiver Chart mit Hover-Tooltips
- Einstellungen werden automatisch gespeichert (`hypothekenrechner_settings.json`)
- Zweisprachig: Deutsch / Englisch (Auswahl beim ersten Start)

### Voraussetzungen
- Python 3.8 oder neuer
- matplotlib

```bash
pip install matplotlib
```

### Starten
```bash
python hypothekenrechner.py
```

Beim **ersten Start** erscheint ein Sprachauswahl-Dialog.  
Ab dem zweiten Start wird die gespeicherte Sprache automatisch geladen.

### Eingaben
| Feld | Beschreibung |
|---|---|
| Kaufpreis | Kaufpreis der Immobilie |
| Eigenkapital | Eigenes Kapital (inkl. % Anzeige) |
| Nebenkosten | Grunderwerbsteuer, Notar, Grundbuch etc. |
| Zinssatz | Effektiver Jahreszins |
| Zinsbindung | Laufzeit in Jahren |
| Monatsrate | Gewünschte monatliche Rate |
| Zielrestschuld | Gewünschte Restschuld nach Laufzeit (%) |
| Guthabenzins | Zinssatz beim Sparen |
| Immo-Wertsteigerung | Jährliche Wertsteigerung der Immobilie |

### Tastatursteuerung
- **Tab / Shift+Tab** — nächster / vorheriger Slider
- **← →** Pfeiltasten — Slider um einen Schritt bewegen
- **Klick** auf Slider — Fokus setzen

---

## 🇬🇧 English

### Features
- Annuity loan calculation with all relevant parameters
- Savings comparison: monthly savings vs. property purchase
- Configurable property appreciation rate
- Net property value: honest comparison including interest and ancillary costs
- Interactive chart with hover tooltips
- Settings automatically saved (`hypothekenrechner_settings.json`)
- Bilingual: German / English (selected on first start)

### Requirements
- Python 3.8 or newer
- matplotlib

```bash
pip install matplotlib
```

### Run
```bash
python hypothekenrechner.py
```

On **first launch**, a language selection dialog will appear.  
On subsequent launches, the saved language is loaded automatically.

### Inputs
| Field | Description |
|---|---|
| Purchase Price | Property purchase price |
| Equity | Own capital (with % display) |
| Ancillary Costs | Transfer tax, notary, land registry etc. |
| Interest Rate | Effective annual interest rate |
| Fixed Rate Period | Duration in years |
| Monthly Payment | Desired monthly payment |
| Target Residual Debt | Desired remaining debt after period (%) |
| Savings Interest | Interest rate when saving |
| Property Appreciation | Annual property value increase |

### Keyboard Navigation
- **Tab / Shift+Tab** — next / previous slider
- **← →** Arrow keys — move slider by one step
- **Click** on slider — set focus

---

## 📊 Berechnungslogik / Calculation Logic

### Immo-Nettovermögen / Net Property Value

```
Immo-Nettovermögen = Immowert nach Laufzeit
                   - Restschuld
                   - gezahlte Zinsen
                   - Nebenkosten
```

Zinsen und Nebenkosten sind wie "verbranntes Geld" — sie fließen nicht in den Vermögenswert ein.  
Interest and ancillary costs are "burned money" — they do not contribute to the asset value.

### Vorteil Sparer / Saver Advantage

```
Vorteil = Sparguthaben - Immo-Nettovermögen
  + = Sparen ist besser / Saving is better
  - = Immokauf ist besser / Buying is better
```

---

## 🔧 Als .exe kompilieren / Compile to .exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed hypothekenrechner.py
```

Die fertige `.exe` liegt in `dist/hypothekenrechner.exe`.  
The finished `.exe` is located in `dist/hypothekenrechner.exe`.

---

## 📁 Dateien / Files

| Datei / File | Beschreibung / Description |
|---|---|
| `hypothekenrechner.py` | Hauptprogramm / Main program |
| `hypothekenrechner_settings.json` | Gespeicherte Einstellungen (automatisch erstellt) / Saved settings (auto-created) |
| `README.md` | Diese Datei / This file |

---

## 📜 Lizenz / License

**Apache License 2.0**

Du darfst diesen Code frei nutzen, verändern und weitergeben — auch kommerziell.  
**Bedingung:** Der Ursprung (dieses Repository) muss immer genannt werden.  
Änderungen müssen als solche gekennzeichnet werden.

You are free to use, modify and distribute this code — including commercially.  
**Condition:** The origin (this repository) must always be credited.  
Modifications must be marked as such.

Copyright 2025 [IschNehmDirGleichDemTabletWeg](https://github.com/IschNehmDirGleichDemTabletWeg)  
→ https://github.com/IschNehmDirGleichDemTabletWeg/HypothekenRechner
