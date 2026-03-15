import os
import csv
from datetime import datetime, timedelta
from rich.table import Table
from rich.console import Console
from datetime import datetime
import matplotlib.pyplot as plt

# -----------------------------
# CONSTANTEN
# -----------------------------

DATE_FORMAT = "%d-%m-%Y"
DATE_PATH = os.path.join("data", "date_today.txt")
BOUGHT_PATH = os.path.join("data", "bought.csv")
SOLD_PATH = os.path.join("data", "sold.csv")
EXP_PATH = os.path.join("data","expired.csv")


# -----------------------------
# DATUMFUNCTIES
# -----------------------------

def get_date():
    """Lees de huidige SuperPy-datum uit het bestand."""
    with open(DATE_PATH, "r") as f:
        return f.read().strip()


def set_date(new_date):
    """Schrijf een nieuwe datum naar het datum-bestand."""
    with open(DATE_PATH, "w") as f:
        f.write(new_date)


def advance_time(days):
    """Verzet de SuperPy-datum met X dagen."""
    current = get_date()
    current_date = datetime.strptime(current, DATE_FORMAT)

    new_date = current_date + timedelta(days=days)
    formatted = new_date.strftime(DATE_FORMAT)

    set_date(formatted)
    print("Datum aangepast naar:", formatted)


def reset_date():
    """Zet de SuperPy-datum terug naar vandaag."""
    today = datetime.today().strftime(DATE_FORMAT)
    set_date(today)
    print("Datum gereset naar vandaag:", today)

def parse_date(date_str):
    return datetime.strptime(date_str, "%d-%m-%Y")

def is_same_day(d1, d2):
    return d1.date() == d2.date()

def is_same_week(d1, d2):
    return d1.isocalendar()[:2] == d2.isocalendar()[:2]

def is_same_month(d1, d2):
    return d1.year == d2.year and d1.month == d2.month


# -----------------------------
# CSV FUNCTIES
# -----------------------------

# ___ KOPEN ___

def read_bought_csv():
    """Lees alle gekochte producten uit bought.csv."""
    if not os.path.exists(BOUGHT_PATH):
        return []

    with open(BOUGHT_PATH, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        return list(reader)
    

def show_bought_table():
    """Print alle items uit bought.csv in tabelvorm."""
    rows = read_bought_csv()

    if not rows:
        print("Geen ingekochte producten gevonden.")
        return

    # Kolomnamen bepalen, None verwijderen
    headers = [h for h in rows[0].keys() if h]

    # Kolombreedtes bepalen (None → "")
    col_widths = {
        h: max(
            len(h),
            max(len((row.get(h) or "")) for row in rows)
        )
        for h in headers
    }

    # Header printen
    header_line = " | ".join(h.ljust(col_widths[h]) for h in headers)
    separator = "-+-".join("-" * col_widths[h] for h in headers)

    print(header_line)
    print(separator)

    # Rijen printen
    for row in rows:
        line = " | ".join((row.get(h) or "").ljust(col_widths[h]) for h in headers)
        print(line)


def buy_product(product_name, buy_price, amount, expiration_date):
    
    # Bestaat het bestand?
    file_exists = os.path.isfile(BOUGHT_PATH)

    # Lees bestaande regels
    rows = []
    if file_exists:
        with open(BOUGHT_PATH, "r", newline="") as f:
            reader = csv.DictReader(f, delimiter=';')
            rows = list(reader)

    # Nieuw ID bepalen
    if rows and "id" in rows[-1]:
        new_id = int(rows[-1]["id"]) + 1
    else:
        new_id = 1

    # Huidige SuperPy-datum
    buy_date = get_date()

    # Schrijf naar CSV
    with open(BOUGHT_PATH, "a", newline="") as f:
        fieldnames = ["id", "product_name", "buy_date", "buy_price", "expiration_date"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')

        # Header schrijven als bestand leeg is
        if not file_exists or os.path.getsize(BOUGHT_PATH) == 0:
            writer.writeheader()

        writer.writerow({
            "id": new_id,
            "product_name": product_name,
            "buy_date": buy_date,
            "buy_price": buy_price,
            "expiration_date": expiration_date
        })

    print(f"Gekocht: {product_name} voor €{buy_price}, exp: {expiration_date}")



# ___ VERKOPEN ___

def show_sold_table():
    """Print alle items uit sold.csv in tabelvorm."""
    rows = read_sold_csv()

    if not rows:
        print("Geen verkochte producten gevonden.")
        return

    # Kolomnamen bepalen, None verwijderen
    headers = [h for h in rows[0].keys() if h]

    # Kolombreedtes bepalen
    col_widths = {
        h: max(
            len(h),
            max(len((row.get(h) or "")) for row in rows)
        )
        for h in headers
    }

    # Header printen
    header_line = " | ".join(h.ljust(col_widths[h]) for h in headers)
    separator = "-+-".join("-" * col_widths[h] for h in headers)

    print(header_line)
    print(separator)

    # Rijen printen
    for row in rows:
        line = " | ".join((row.get(h) or "").ljust(col_widths[h]) for h in headers)
        print(line)


def read_sold_csv():
    if not os.path.exists(SOLD_PATH):
        return []
    with open(SOLD_PATH, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        return list(reader)

def append_sold_row(row):
    file_exists = os.path.exists(SOLD_PATH)
    with open(SOLD_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys(), delimiter=";")
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def write_bought_csv(rows):
    if not rows:
        return
    with open(BOUGHT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)

def sell_product(product_name, sell_price):
    """Verkoop één item uit de voorraad en verwerk dit in sold.csv."""
    bought_items = read_bought_csv()
    today = datetime.strptime(get_date(), "%d-%m-%Y")

    # Zoek een item dat overeenkomt en niet verlopen is
    for item in bought_items:
        if item["product_name"] != product_name:
            continue

        exp = item.get("expiration_date")
        if exp:
            exp_date = datetime.strptime(exp, "%d-%m-%Y")
            if exp_date < today:
                continue  # item is verlopen → niet verkoopbaar


        # Nieuw ID bepalen voor sold.csv
        sold_rows = read_sold_csv()

        if sold_rows and "id" in sold_rows[-1]:
            new_id = int(sold_rows[-1]["id"]) + 1
        else:
            new_id = 1
     
        # Verkoop registreren   
        sold_row = {
            "id": new_id,
            "bought_id": item["id"],
            "product_name": product_name,
            "sell_date": get_date(),
            "sell_price": str(sell_price)
           
        }
        append_sold_row(sold_row)

        print(f"Product verkocht: {product_name} voor €{sell_price}")
        return

    print(f"Geen verkoopbaar item gevonden voor: {product_name}")


# ___ HOUDBAARHEID ___

def read_expired_csv():
    if not os.path.isfile(EXP_PATH):
        return []
    with open(EXP_PATH, "r", newline="") as f:
        reader = csv.DictReader(f, delimiter=';')
        return list(reader)


def append_expired_row(row):
    file_exists = os.path.isfile(EXP_PATH)
    with open(EXP_PATH, "a", newline="") as f:
        fieldnames = [
            "id",
            "bought_id",
            "product_name",
            "buy_date",
            "buy_price",
            "expiration_date",
            "expired_on"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def remove_expired_products():
    """Zoek verlopen producten en registreer ze in expired.csv zonder bought.csv te wijzigen."""
    bought_items = read_bought_csv()
    expired_rows = read_expired_csv()
    today = datetime.strptime(get_date(), "%d-%m-%Y")

    # Verzamel alle bought_id's die al in expired.csv staan 
    already_expired_ids = {row["bought_id"] for row in expired_rows}
    
    expired_items = []

    # Zoek verlopen items die nog NIET in expired.csv staan
    for item in bought_items:
        exp = item.get("expiration_date")
        if not exp:
            continue 
        
        exp_date = datetime.strptime(exp, "%d-%m-%Y")
        
        if exp_date < today and item["id"] not in already_expired_ids: 
            expired_items.append(item)

    # Verlopen items wegschrijven
    next_id = int(expired_rows[-1]["id"]) + 1 if expired_rows else 1

    for item in expired_items:
        append_expired_row({
            "id": next_id,
            "bought_id": item["id"],
            "product_name": item["product_name"],
            "buy_date": item["buy_date"],
            "buy_price": item["buy_price"],
            "expiration_date": item["expiration_date"],
            "expired_on": get_date()
        })
        next_id += 1

    print(f"{len(expired_items)} producten geregistreerd als verlopen.")

from rich.table import Table
from rich.console import Console

def show_expired_table():
    """Toon verlopen producten in een Rich-tabel."""
    rows = read_expired_csv()

    if not rows:
        print("Geen verlopen producten gevonden.")
        return

    console = Console()
    table = Table(title="Verlopen producten", show_lines=True)

    table.add_column("ID", justify="right")
    table.add_column("Product")
    table.add_column("Gekocht op")
    table.add_column("Inkoopprijs", justify="right")
    table.add_column("Houdbaar tot")
    table.add_column("Verlopen op")

    total_cost = 0.0

    for row in rows:
        price = float(row["buy_price"].replace(",", "."))
        total_cost += price

        table.add_row(
            row["id"],
            row["product_name"],
            row["buy_date"],
            row["buy_price"],
            row["expiration_date"],
            f"[red]{row['expired_on']}[/red]"
        )

    console.print(table)
    console.print(f"[bold]Totaal verlopen producten:[/bold] {len(rows)}")
    console.print(f"[bold red]Totale verspilde inkoopkosten:[/bold red] €{total_cost:.2f}")


# -----------------------------
# BEREKENINGEN
# -----------------------------

# ___ VOORRAAD ___

def get_inventory():
    bought = read_bought_csv()
    sold = read_sold_csv()
    expired = read_expired_csv()

    sold_ids = {row["bought_id"] for row in sold}
    expired_ids = {row["bought_id"] for row in expired}

    inventory = [item for item in bought 
                 if item["id"] not in sold_ids 
                 and item["id"] not in expired_ids]

    return inventory


def show_inventory_table():
    """Toon de huidige voorraad in een Rich-tabel met kleurcodes voor houdbaarheid."""
    rows = get_inventory()

    if not rows:
        print("Geen producten op voorraad.")
        return
    
    # --- Aantal per product berekenen --- 
    counts = {} 
    for row in rows: 
        name = row["product_name"] 
        counts[name] = counts.get(name, 0) + 1

    console = Console()
    table = Table(title="Voorraad", show_lines=True)

    # Kolommen
    table.add_column("ID", justify="right")
    table.add_column("Product")
    table.add_column("Aantal", justify="right")
    table.add_column("Gekocht op")
    table.add_column("Inkoopprijs", justify="right")
    table.add_column("Houdbaar tot")
    table.add_column("Status")

    today = datetime.strptime(get_date(), "%d-%m-%Y")
    ALMOST_EXPIRED_DAYS = 2

    for row in rows:
        exp_date = datetime.strptime(row["expiration_date"], "%d-%m-%Y")
        days_left = (exp_date - today).days

        # Status + kleur bepalen
        if days_left < 0:
            status = "[bold red]Verlopen[/bold red]"
        elif days_left <= ALMOST_EXPIRED_DAYS:
            status = f"[yellow]Bijna verlopen ({days_left} dagen)[/yellow]"
        else:
            status = f"[green]OK ({days_left} dagen)[/green]"

        table.add_row(
            row["id"],
            row["product_name"],
            str(counts[row["product_name"]]),
            row["buy_date"],
            row["buy_price"],
            row["expiration_date"],
            status
        )

    console.print(table)
    
    # Extra overzicht onderaan 
    console.print("\n[bold]Totaal per product:[/bold]") 
    for product, amount in counts.items():
        console.print(f" - {product}: {amount} stuks") 
        
    console.print(f"\n[bold]Totaal op voorraad:[/bold] {len(rows)} producten.")

#___ GRAFIEK VAN OMZET PER DAG ___

def get_revenue_per_day():
    sold = read_sold_csv()
    revenue_per_day = {}

    for row in sold:
        date = row["sell_date"]
        price = float(row["sell_price"].replace(",", "."))
        revenue_per_day[date] = revenue_per_day.get(date, 0) + price

    return revenue_per_day

def plot_revenue_per_day():
    data = get_revenue_per_day()

    if not data:
        print("Geen verkoopdata beschikbaar om te plotten.")
        return

    # Sorteren op datum
    dates = sorted(data.keys(), key=lambda d: datetime.strptime(d, "%d-%m-%Y"))
    values = [data[d] for d in dates]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, values, marker="o", linestyle="-", color="blue")

    plt.title("Omzet per dag")
    plt.xlabel("Datum")
    plt.ylabel("Omzet (€)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)

    plt.show()

#___ FINANCIEEL OVERZICHT ___

# Omzet berekenen
def calculate_revenue():
    sold_items = read_sold_csv()
    revenue = 0.0

    for item in sold_items:
        try:
            price = item["sell_price"].replace(",", ".").replace("€", "").strip()
            revenue += float(price)
        except:
            pass

    return revenue

# Inkoopprijs van verkochte items berekenen (Cost Of Goods Sold)
def calculate_cogs():
    sold_items = read_sold_csv()
    bought_items = read_bought_csv()

    # Maak lookup tabel: id → buy_price
    buy_lookup = {row["id"]: row["buy_price"] for row in bought_items}

    cogs = 0.0
    for item in sold_items:
        bought_id = item["bought_id"]
        if bought_id in buy_lookup:
            try:
                price = buy_lookup[bought_id].replace(",", ".").replace("€", "").strip()
                cogs += float(price)
            except:
                pass

    return cogs

# Verspilling berekenen
def calculate_expired_cost():
    if not os.path.isfile(EXP_PATH):
        return 0.0

    with open(EXP_PATH, "r", newline="") as f:
        reader = csv.DictReader(f, delimiter=';')
        rows = list(reader)

    total = 0.0
    for row in rows:
        try:
            price = row["buy_price"].replace(",", ".").replace("€", "").strip()
            total += float(price)
        except:
            pass

    return total

# Winst berekenen
def calculate_profit(include_expired=False):
    revenue = calculate_revenue()
    cogs = calculate_cogs()
    profit = revenue - cogs

    if include_expired:
        expired_cost = calculate_expired_cost()
        profit -= expired_cost

    return profit

#___ RAPPORTAGE ___

def calculate_financials(period="total"):
    today = parse_date(get_date())

    sold = read_sold_csv()
    bought = read_bought_csv()
    expired = read_expired_csv()

    buy_lookup = {row["id"]: row["buy_price"] for row in bought}

    revenue = 0.0
    cogs = 0.0
    expired_cost = 0.0

    for item in sold:
        sell_date = parse_date(item["sell_date"])
        if period == "day" and not is_same_day(sell_date, today):
            continue
        if period == "week" and not is_same_week(sell_date, today):
            continue
        if period == "month" and not is_same_month(sell_date, today):
            continue

        revenue += float(item["sell_price"].replace(",", "."))
        cogs += float(buy_lookup[item["bought_id"]].replace(",", "."))

    for item in expired:
        exp_date = parse_date(item["expired_on"])
        if period == "day" and not is_same_day(exp_date, today):
            continue
        if period == "week" and not is_same_week(exp_date, today):
            continue
        if period == "month" and not is_same_month(exp_date, today):
            continue

        expired_cost += float(item["buy_price"].replace(",", "."))

    profit = revenue - cogs
    net_profit = profit - expired_cost

    return {
        "revenue": revenue,
        "cogs": cogs,
        "profit": profit,
        "expired_cost": expired_cost,
        "net_profit": net_profit
    }


def plot_financials(period="total"):
    data = calculate_financials(period)

    labels = ["Omzet", "COGS", "Brutowinst", "Verspilling", "Netto winst"]
    values = [
        data["revenue"],
        data["cogs"],
        data["profit"],
        data["expired_cost"],
        data["net_profit"]
    ]

    colors = ["green", "orange", "blue", "red", "purple"]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color=colors)

    plt.title(f"Financieel overzicht ({period})")
    plt.ylabel("Bedrag (€)")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()



from rich.table import Table
from rich.console import Console

def report_financials(period="total"):
    data = calculate_financials(period)

    revenue = data["revenue"]
    cogs = data["cogs"]
    profit = data["profit"]
    expired_cost = data["expired_cost"]
    net_profit = data["net_profit"]

    console = Console()
    table = Table(title=f"Financieel rapport ({period})", show_lines=True)

    table.add_column("Categorie")
    table.add_column("Bedrag (€)", justify="right")

    table.add_row("Omzet (Revenue)", f"{revenue:.2f}")
    table.add_row("Inkoopkosten (COGS)", f"{cogs:.2f}")
    table.add_row("Brutowinst", f"{profit:.2f}")
    table.add_row("Verspilling", f"[red]{expired_cost:.2f}[/red]")

    if net_profit >= 0:
        table.add_row("Netto winst", f"[green]{net_profit:.2f}[/green]")
    else:
        table.add_row("Netto winst", f"[red]{net_profit:.2f}[/red]")

    console.print(table)

    # --- Grafiek tonen ---
    plot_financials(period)

def plot_inventory_counts():
    rows = get_inventory()
    if not rows:
        print("Geen voorraad om te plotten.")
        return

    # Aantal per product
    counts = {}
    for row in rows:
        name = row["product_name"]
        counts[name] = counts.get(name, 0) + 1

    products = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(10, 5))
    plt.bar(products, values, color="skyblue")

    plt.title("Voorraad per product")
    plt.xlabel("Product")
    plt.ylabel("Aantal stuks")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
