# Imports
import argparse
import csv
from datetime import date, datetime, timedelta
import os
from functions import advance_time, get_date, reset_date, show_bought_table, show_sold_table, show_inventory_table, sell_product, buy_product,  remove_expired_products, show_expired_table,calculate_revenue, calculate_profit, calculate_cogs, report_financials, calculate_expired_cost, plot_revenue_per_day, plot_inventory_counts
import matplotlib.pyplot as plt
from rich.table import Table 
from rich.console import Console


# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--advance-time", type=int, 
                    help="Verzet de datum met X dagen")
    parser.add_argument("--reset-date", action="store_true",
                    help="Reset de SuperPy-datum naar vandaag")
    parser.add_argument("--show-bought", action="store_true",
                    help="Toon alle ingekochte producten in tabelvorm")
    parser.add_argument("--buy", nargs=3, metavar=("PRODUCT", "PRICE", "EXPIRATION"),
                    help="Koop een product met prijs en houdbaarheidsdatum (DD-MM-YYYY)")
    parser.add_argument("--show-sold", action="store_true",
                    help="Toon alle verkochte producten in tabelvorm")
    parser.add_argument("--inventory", action="store_true",
                    help="Toon de huidige voorraad inclusief expiratie-status")
    parser.add_argument("--sell", nargs=2, metavar=("PRODUCT", "PRICE"),
                    help="Verkoop een product voor een bepaalde prijs")
    parser.add_argument("--clean-expired", action="store_true",
                    help="Verwijder verlopen producten uit de voorraad en schrijf ze weg naar expired.csv")
    parser.add_argument("--show-expired", action="store_true",
                    help="Toon alle verlopen producten in tabelvorm")
    parser.add_argument("--report-profit", action="store_true",
                    help="Toon totale winst en omzet")
    parser.add_argument("--report-profit-net", action="store_true",
                    help="Toon winst inclusief verspilling")
    parser.add_argument("--report", choices=["day", "week", "month", "total"],
                    help="Toon financieel rapport voor dag/week/maand/totaal")
    parser.add_argument("--plot-revenue", action="store_true",
                    help="Toon een grafiek van omzet per dag")
    parser.add_argument(    "--plot-inventory",    action="store_true",
                    help="Toon een grafiek van de voorraad per product")





    args = parser.parse_args()

    if args.advance_time is not None:
         advance_time(args.advance_time)
         return
    
    if args.reset_date:
        reset_date()
        return

    if args.show_bought:
        show_bought_table()
        return
  
    if args.buy:
        product, price, expiration = args.buy
        buy_product(product, float(price), 1, expiration)
        return

    if args.show_sold:
        show_sold_table()
        return
    
    if args.inventory:
        show_inventory_table()
        return

    if args.sell:
        product, price = args.sell
        sell_product(product, float(price))
        return
    
    if args.clean_expired:
        remove_expired_products()
        return

    if args.show_expired:
        show_expired_table()
        return

    if args.report:
        report_financials(args.report)
        return

    if args.report_profit:
        revenue = calculate_revenue()
        cogs = calculate_cogs()
        profit = calculate_profit()
        
        console = Console()
        table = Table(title="Winstoverzicht")

        table.add_column("Categorie")
        table.add_column("Bedrag (€)", justify="right")

        table.add_row("Omzet", f"{revenue:.2f}")
        table.add_row("Inkoopprijs", f"{cogs:.2f}")

        # Winst kleurcoderen
        if profit < 0:
            profit_str = f"[red]{profit:.2f}[/red]"
        else:
            profit_str = f"[green]{profit:.2f}[/green]"

        table.add_row("Winst", profit_str)

        console.print(table)
        return


    if args.report_profit_net:
        revenue = calculate_revenue()
        cogs = calculate_cogs()
        expired = calculate_expired_cost()
        profit = calculate_profit(include_expired=True)
        console = Console() 
        table = Table(title="Netto winst (incl. verspilling)", show_lines=True) 
        
        table.add_column("Categorie") 
        table.add_column("Bedrag (€)", justify="right") 
        
        table.add_row("Omzet", f"{revenue:.2f}") 
        table.add_row("Inkoopprijs", f"{cogs:.2f}") 
        table.add_row("Kosten verspilling", f"[red]{expired:.2f}[/red]") 
        
        # Netto winst kleurcoderen
        if profit >= 0:
            table.add_row("Netto winst", f"[green]{profit:.2f}[/green]") 
        else: 
            table.add_row("Netto winst", f"[red]{profit:.2f}[/red]") 
            
        console.print(table) 
        return

    # Standaard gedrag: toon huidige datum 
    print("De huidige SuperPy-datum:", get_date())

    if args.plot_revenue:
        plot_revenue_per_day()
        return

    if args.plot_inventory:
        plot_inventory_counts()
    return


if __name__ == "__main__":
    main()
