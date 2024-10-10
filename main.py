import argparse
import scraper
import panda


if __name__ == "__main__":

    argparse.ArgumentParser(
        description="This is a simple program that prints out the input arguments"
    )
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--liga",
        help="Cislo ligy, 0 = extraliga, 1 = 1. liga, 2 = 2. liga",
        default=0,
        action="store",
    )
    parser.add_argument(
        "--start", help="Pocatecni sezona, napr. 2017", required=True, action="store"
    )
    parser.add_argument(
        "--end",
        help="Koncova sezona, napr. 2018, pokud nezadano, tak se bere jen jedna sezona = start",
        required=False,
        action="store",
    )
    parser.add_argument(
        "--output", help="Vystupni soubor", required=False, default="output.csv"
    )
    parser.add_argument(
        "--roky",
        help="Vypise vsechny roky, ktere jsou dostupne pro danou ligu",
        required=False,
        default=False,
        action="store_true",
    )
    parser.add_argument("--system", help="System, 0 = body, 1 = skore +-", default=0)

    args = parser.parse_args()
    print(args.liga, args.start, args.end, args.output, args.roky, args.system)
    scr = scraper.Scraper()
    scr.get_league_available_years(args.liga)
    if args.roky:
        print(scr.get_league_available_years(args.liga))

    if args.end is None:
        args.end = args.start

    tabuky = scr.get_league_tables(args.liga, args.start, args.end)

    tables = panda.Tables(tabuky)
    for t in tables.get_tables():
        t.apply_system(args.system)
        print(t.print_simple())
