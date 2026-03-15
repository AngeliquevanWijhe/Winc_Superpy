---

# **SuperPy – Voorraadbeheer & Financieel Dashboard**

SuperPy is een command‑line applicatie voor het beheren van voorraad, verkopen, inkoop, houdbaarheid en financiële rapportages. Het systeem ondersteunt tijdreizen, automatische verwerking van verlopen producten, Rich‑tabellen en grafieken via matplotlib.

Druk op Ctrl + Shift + V om de Markdown‑preview te openen

---

## 📦 Functionaliteiten

### **Voorraadbeheer**
- Producten inkopen (`--buy`)
- Producten verkopen (`--sell`)
- Voorraad bekijken met houdbaarheidsstatus
- Automatische detectie van verlopen producten
- Verlopen producten registreren in `expired.csv`

### **Financieel overzicht**
- Omzet, inkoopprijs, winst en verspilling berekenen
- Financiële rapportages per:
  - dag
  - week
  - maand
  - totaal
- Grafische weergave van financiële resultaten
- Omzet per dag grafiek

### **Tijdbeheer**
- Datum vooruit zetten (`--advance-time`)
- Datum resetten naar vandaag (`--reset-date`)

### **Rapportages**
- Rich‑tabellen voor:
  - ingekochte producten
  - verkochte producten
  - voorraad
  - verlopen producten
- Financiële rapporten met grafieken

---

## 📁 Bestandsstructuur

```
superpy/
│
├── main.py
├── functions.py
│
└── data/
    ├── bought.csv
    ├── sold.csv
    ├── expired.csv
    └── date_today.txt
```

---

## 🚀 Installatie

### 1. Vereisten
- Python 3.12 (aanbevolen)
- pip modules:
  ```
  pip install rich matplotlib
  ```

### 2. Project starten
Zorg dat je in de projectmap staat:

```
cd superpy
```

---

## 🧭 Gebruik (CLI‑commando’s)

### **Datumbeheer**
| Command | Beschrijving |
|--------|--------------|
| `--advance-time X` | Verzet de datum met X dagen |
| `--reset-date` | Zet datum terug naar vandaag |

---

### **Inkoop & verkoop**
| Command | Voorbeeld | Beschrijving |
|--------|-----------|--------------|
| `--buy PRODUCT PRICE EXP` | `--buy appel 1.20 10-03-2026` | Koop product |
| `--sell PRODUCT PRICE` | `--sell appel 2.00` | Verkoop product |

---

### **Tabellen bekijken**
| Command | Beschrijving |
|--------|--------------|
| `--show-bought` | Toon ingekochte producten |
| `--show-sold` | Toon verkochte producten |
| `--inventory` | Toon voorraad met houdbaarheid |
| `--show-expired` | Toon verlopen producten |

---

### **Verlopen producten verwerken**
| Command | Beschrijving |
|--------|--------------|
| `--clean-expired` | Verplaats verlopen producten naar expired.csv |

---

### **Financiële rapportages**
| Command | Beschrijving |
|--------|--------------|
| `--report day` | Rapport van vandaag |
| `--report week` | Rapport van deze week |
| `--report month` | Rapport van deze maand |
| `--report total` | Rapport van alle data |
| `--report-profit` | Toon omzet, inkoopprijs en winst |
| `--report-profit-net` | Toon winst inclusief verspilling |

---

### **Grafieken**
| Command | Beschrijving |
|--------|--------------|
| `--plot-revenue`   | Omzet per dag grafiek |
| `--plot-inventory` | Voorraad per product grafiek |

---

## 📊 Voorbeeld: financieel rapport

```
python main.py --report week
```

Toont:

- Rich‑tabel met omzet, inkoopprijs, winst en verspilling
- Automatisch een grafiek met dezelfde waarden

---

## 📈 Voorbeeld: omzet per dag grafiek

```
python main.py --plot-revenue
```

---

## 🧪 Voorbeeld: producten kopen en verkopen

```
python main.py --buy banaan 0.50 05-03-2026
python main.py --sell banaan 1.00
```

---

## 🗂 CSV‑bestanden

### **bought.csv**
Bevat alle ingekochte producten.

### **sold.csv**
Bevat alle verkochte producten.

### **expired.csv**
Bevat alle verlopen producten.

### **date_today.txt**
Bevat de huidige SuperPy‑datum.

---

## 🛠 Ontwikkelaarsinformatie

### Belangrijkste modules
- `functions.py` bevat:
  - CSV‑functies
  - datumfuncties
  - voorraadberekeningen
  - financiële berekeningen
  - grafiekfuncties
  - rapportages

- `main.py` bevat:
  - CLI‑argumenten
  - command‑router

---

## ⭐ Noemenswaardige functies

### Gebruik van RICH module
De RICH‑module maakt de financiële overzichten en rapportages eenvoudiger leesbaar en visueel aantrekkelijker.

### Gebruik van de matplotlib module
Met de matplotlib‑module zijn grafieken beschikbaar die een duidelijk beeld geven van de omzet, winst en voorraad.

### Gebruik van CSV bestanden
CSV‑bestanden voor inkoop, verkoop en verspilling worden automatisch gevuld door de commando’s van de applicatie, waardoor alle gegevens overzichtelijk en gestructureerd worden opgeslagen.


---