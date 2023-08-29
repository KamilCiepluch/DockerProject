import requests
import json
import argumentsHelper
import plotHelper
URL = "http://localhost:80"


def show_collections():
    url = URL + "/collections"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Dostepne kolekcje:")
            for res in response.json():
                print(f"\t-{res}")
        else:
            print("Błąd przy żądaniu. Status:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Wystąpił błąd przy żądaniu:", e)


def get_collections():
    url = URL + "/collections"
    response = requests.get(url)
    return response.json()


def get_skins_from_collection(collection_name):
    url = URL + "/skins"
    data = {"collection": collection_name}

    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            print(collection_name+":")
            for skin in response_data:
                print(f"\t{skin[0].ljust(50)}   ({skin[1]})")
        else:
            print("Błąd przy żądaniu. Status:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Wystąpił błąd przy żądaniu:", e)

def get_compered_collection(name1, name2, args):
    url = URL + "/compere_collections"
    data = {"collection1": name1,
            "collection2": name2,
            "args": args}

    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            collection1_prices = response_data['collection1']
            collection2_prices = response_data['collection2']
            weeks = response_data['weeks']
            plotHelper.create_plots(weeks, collection1_prices, collection2_prices, title="")

        else:
            print("Błąd przy żądaniu. Status:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Wystąpił błąd przy żądaniu:", e)


def get_skin_weekly_price(selected_collection, option, args):
    url = URL + "/skin_weekly_prices"

    data = {"selected_collection": selected_collection,
            "option": option,
            "args": args}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            print("Błąd przy żądaniu. Status:", response.status_code)

    except requests.exceptions.RequestException as e:
        print("Wystąpił błąd przy żądaniu:", e)
    except Exception:
        print("Podano niepoprawne dane")


def print_skin_weekly_price(selected_collection, response_data):
    weekly_prices = response_data['weekly_prices']
    weeks = response_data['weeks_numbers']

    if option == 'all':
        plotHelper.create_plot(weeks, weekly_prices,
                               f"Weekly changes for {selected_collection} - All skins")
    elif option == 'skin':
        name = argumentsHelper.extract_name(args)
        weapon = argumentsHelper.extract_weapon(args)
        plotHelper.create_plot(weeks, weekly_prices,
                               f"Weekly changes for {selected_collection} - {weapon} | {name}")
    elif option == 'quality':
        plotHelper.create_plot(weeks, weekly_prices,
                               f"Weekly changes for {selected_collection} - {args}")
    else:
        print("Podano niepprawna opcje")

def get_increase_intervals(selected_collection, option, args, label='tygodnia', shift=3):
    url = URL + "/increase_interval"

    data = {"selected_collection": selected_collection,
            "option": option,
            "args": args}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            data = response.json()
            increase_intervals = data['intervals']
            prices = data['weekly_prices']
            print("Okresy wzrostowe:")
            for start, end in increase_intervals:
                formatted_start = f"{start:{shift}}"
                formatted_end = f"{end:{shift}}"
                change = round(((prices[end] - prices[start]) / prices[start]) * 100, 2)
                formatted_change = f"{change:{shift}}"
                print(f"\tod {label} {formatted_start} do {label} {formatted_end} \t"
                      f"Ceny w przedziale: {prices[start]:{shift + 2}} - {prices[end]:{shift + 2}}"
                      f"\tWartość wzorsła o: {formatted_change}%")
        else:
            print("Błąd przy żądaniu. Status:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Wystąpił błąd przy żądaniu:", e)


def get_decrease_intervals(selected_collection, option, args, label='tygodnia', shift=3):
    url = URL + "/decrease_interval"

    data = {"selected_collection": selected_collection,
            "option": option,
            "args": args}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            data = response.json()
            decrease_intervals = data['intervals']
            prices = data['weekly_prices']
            print("Okresy spadkowe:")
            for start, end in decrease_intervals:
                formatted_start = f"{start:{shift}}"
                formatted_end = f"{end:{shift}}"
                change = round(((prices[end] - prices[start]) / prices[start]) * 100, 2)
                formatted_change = f"{change:{shift}}"
                print(f"\tod {label} {formatted_start} do {label} {formatted_end} \t"
                      f"Ceny w przedziale: {prices[start]:{shift + 2}} - {prices[end]:{shift + 2}}"
                      f"\tWartość spadła o: {formatted_change}%")
        else:
            print("Błąd przy żądaniu. Status:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Wystąpił błąd przy żądaniu:", e)


def show_wears_info():
    dictionary = {
        "fc": "Factory New",
        "mw": "Minimal Wear",
        "ft": "Field-Tested",
        "ww": "Well-Worn",
        "bs": "Battle-Scarred"
    }
    print("Wears:")
    for dic in dictionary:
        print(f"\t{dic}  {dictionary.get(dic)}")


def show_quality_info():
    dictionary = {
        "gold": "Rare Special Items",
        "red": "Covert Skins",
        "pink": "Classified Skins",
        "purple": "Restricted Skins",
        "blue": "Mil-Spec Skins",
        "light_blue": "Industrial Grade Skins",
        "gray": "Consumer Grade Skins",
        "rar": "Rare Special Items",
        "cov": "Covert Skins",
        "cla": "Classified Skins",
        "res": "Restricted Skins",
        "mil": "Mil-Spec Skins",
        "ind": "Industrial Grade Skins",
        "con": "Consumer Grade Skins",
    }
    print("Quality:")
    for dic in dictionary:
        print(f"\t{dic.ljust(12)}  {dictionary.get(dic)}")


def show_skin_weekly_price_info():

    options = ['all', 'skin', 'quality']
    flags = [[], ["--name", "--weapon", "--W", "--Q"], ["--W", "--Q"]]
    print("Dostepne opcje: ")
    for opt, f in zip(options, flags):
        print(f"\t- {opt.ljust(8)}  dostepne flagi: {f}")


    show_wears_info()
    show_quality_info()

    print("Argumenty:")
    print("\tWeapon:      np.  --weapon Mac-10")
    print("\tSkin Name:   np. --name  Palm")
    print("\tQuality:     np. --Q red pink blue")
    print("\tWear:        np. --W mw ft")


def choose_collection(available_collections):
    collection = None
    while collection not in available_collections:
        collection = input("Podaj kolekcje: ")
        if collection not in available_collections:
            print("Podana kolekcja nie istnieje! Sprobój ponownie")

    return collection





def avaliable_options():
    print("help        - pomoc")
    print("collections - pokaz dostepne kolekcje")
    print("skins       - wyswietla zawartosc kolekcji")
    print("calculate   - analizuj dane z kolekcji")
    print("Intervals   - pokazuje przedzialy w ktorych nastepowaly zmiany cen")
    print("Compare     - porownuje dwie kolekcje w jednakowym okresie czasu")
    print("exit        - zamkniecie aplikacji")


if __name__ == "__main__":

    try:
        available_collections = get_collections()
        avaliable_options()
        while True:
            option = input("Podaj opcje lub help: ")
            options = option.upper().split(" ")

            if 'exit' in option:
                break
            if 'help' in option:
                show_skin_weekly_price_info()

            if 'collections' in option:
                show_collections()
            if 'skins' in option:
                collection = choose_collection(available_collections)
                get_skins_from_collection(collection)
            if 'calculate' in option:
                collection = choose_collection(available_collections)

                opt = None
                while opt is None or opt =='help':
                    opt = input("Podaj opcje lub help jesli chesz wyswietlic liste dostepnych opcji:\n ")

                args = None
                if opt != 'all':
                    args = input("Podaj argumenty:\n")
                data = get_skin_weekly_price(collection, opt, args)

                more_data = input("Czy chcesz wyswietlic dodatkowe statystki? Y/N: ")
                if more_data == 'Y':
                    get_increase_intervals(collection, opt, args)
                    get_decrease_intervals(collection, opt, args)


                print_skin_weekly_price(collection, data)




            if 'intervals' in option:
                collection = choose_collection(available_collections)
                opt = None
                while opt is None or opt == 'help':
                    opt = input("Podaj opcje lub help jesli chesz wyswietlic liste dostepnych opcji:\n ")
                    if opt == 'help':
                        show_skin_weekly_price_info()

                args = None
                if opt != 'all':
                    args = input("Podaj argumenty:\n")

                get_increase_intervals(collection, opt, args)
                get_decrease_intervals(collection, opt, args)

            if 'compare' in option:
                collection1 = choose_collection(available_collections)
                collection2 = choose_collection(available_collections)
                args = input("Podaj argumenty:\n")
                get_compered_collection(collection1, collection2, args)
    except json.decoder.JSONDecodeError:
        print("Nie udało połączyć się z API")

    print("Client closed")