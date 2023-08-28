import json
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy
import numpy as np
import plotly.graph_objects as go
import argumentsHelper
import dbHelper

# chyba złe
def calculate_weekly_averages_with_fill(start_date, dates, values):
    if len(dates) != len(values):
        raise ValueError("Liczba dat i wartości musi być taka sama!")

    weekly_data = {}
    current_date = start_date
    for date, value in zip(dates, values):
        while current_date < date:
            year_week = (current_date.year, current_date.strftime('%U'))
            if year_week not in weekly_data:
                weekly_data[year_week] = {'values': [], 'count': 0}

            # weekly_data[year_week]['values'].append(0)
            # weekly_data[year_week]['count'] += 1
            current_date += timedelta(days=7)

        year_week = (date.year, date.strftime('%U'))
        if year_week not in weekly_data:
            weekly_data[year_week] = {'values': [], 'count': 0}

        weekly_data[year_week]['values'].append(value)
        weekly_data[year_week]['count'] += 1

    weekly_averages = {}
    prev_average = None

    for year_week, data in sorted(weekly_data.items()):
        if data['count'] == 0 and prev_average is not None:
            average = prev_average
        else:
            average = np.sum(data['values']) / len(data['values'])
            prev_average = average

        weekly_averages[year_week] = {'average': average, 'count': data['count']}

    return weekly_averages


def shift_date_start(date):
    week = date.strftime('%U')
    while date.strftime('%U') == week:
        date -= timedelta(days=1)

    date += timedelta(days=1)
    return date

def shift_date_end(date):
    week = date.strftime('%U')
    while date.strftime('%U') == week:
        date += timedelta(days=1)

    date -= timedelta(days=1)
    return date

def convert_dict_to_values_list(dictionary):
    values_list = [entry['values'] for entry in dictionary.values()]
    return values_list


def create_weekly_price_dictionary(start_date, end_date, dates, values):
    if len(dates) != len(values):
        raise ValueError("Liczba dat i wartości musi być taka sama!")

    weekly_data = {}
    start_date = shift_date_start(start_date)
    end_date = shift_date_end(end_date)
    number_of_weeks = int(numpy.ceil((end_date - start_date).days / 7))
    current_date = start_date

    for week in range(0, number_of_weeks):
        w = current_date.strftime('%U')
        if w == '00':
            w = '01'
        year_week = (current_date.year, w)
        weekly_data[year_week] = {'values': [], 'count': 0}
        current_date += timedelta(days=7)

    for date, value in zip(dates, values):
        week = date.strftime('%U')
        if week == '00':
            week = '01'
        year_week = (date.year, week)
        weekly_data[year_week]['values'].append(value)
        weekly_data[year_week]['count'] += 1

    return weekly_data


def calculate_earliest_and_latest_date(operation_data):
    earliest_date = None
    latest_date = None
    for skin in operation_data:
        json_data = json.loads(skin[8])
        dates, values = extract_data_from_json(json_data)
        if earliest_date is None or dates[0] < earliest_date:
            earliest_date = dates[0]
        if latest_date is None or dates[-1] > latest_date:
            latest_date = dates[-1]

    return earliest_date, latest_date


def calculate_weekly_operation_price(operation_data):
    weakly_prices = []
    earliest_date, latest_date = calculate_earliest_and_latest_date(operation_data)
    for skin in operation_data:
        json_data = json.loads(skin[8])
        dates, values = extract_data_from_json(json_data)
        tmp = create_weekly_price_dictionary(earliest_date, latest_date, dates, values)
        expand_weekly_averages(tmp)
        weakly_prices.append(tmp)

    res = None
    for dictionary in weakly_prices:
        val_list = convert_dict_to_values_list(dictionary)
        if res is None:
            res = val_list.copy()
        else:
            res = np.add(res, val_list)

    avg_price_list = np.array(res) / len(weakly_prices)
    rounded_list = [round(number, 2) for number in avg_price_list]
    return rounded_list

def create_list_of_weekly_price(dictionary):
    result_list = []
    for date in dictionary:
        values = dictionary[date]['values']
        avg = 0
        if len(values) != 0:
            avg = (np.sum(values)/len(values))

        result_list.append(avg)
    return result_list

def expand_weekly_averages(dictionary):
    prev = 0
    for date in dictionary:
        val = dictionary[date]['values']
        if len(val) != 0:
            dictionary[date]['values'] = (np.sum(val)/len(val))
            prev = np.sum(dictionary[date]['values'])
        else:
            dictionary[date]['values'] = prev


def calculate_weekly_changes(values):
    weeks = len(values) // 7
    avg_prices = []

    for i in range(weeks):
        week_values = values[i * 7: (i + 1) * 7]
        avg_price = sum(week_values) / 7
        avg_prices.append(avg_price)

    percentage_changes = []

    for i in range(1, len(avg_prices)):
        change = ((avg_prices[i] - avg_prices[i - 1]) / avg_prices[i - 1]) * 100
        percentage_changes.append(change)

    return avg_prices, percentage_changes


def extract_data_from_json(json_data):
    dates = []
    values = []
    for entry in json_data:
        date_str = entry[0]
        value = entry[1]
        date_str_no_tz = date_str.split(':')[0]
        date = datetime.strptime(date_str_no_tz, '%b %d %Y %H')
        tz_offset_str = date_str.split(': ')[1]
        tz_offset_hours = int(tz_offset_str)
        tz_offset = timedelta(hours=tz_offset_hours)
        date += tz_offset

        year = date.year
        month = date.month
        day = date.day
        extracted_date = datetime(year, month, day)

        dates.append(extracted_date)
        values.append(value)

    dates = np.array(dates)
    values = np.array(values)
    return dates, values


def create_price_plot(dates, values):
    # Create a plot
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Value Over Time')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)

    fig = go.Figure()

    # Add a scatter plot
    fig.add_trace(go.Scatter(x=dates, y=values, mode='markers', marker=dict(size=5)))

    # Customize the layout
    fig.update_layout(
        title='Large Number of Data Points',
        xaxis_title='X values',
        yaxis_title='Y values',
        xaxis=dict(type='linear'),
        yaxis=dict(type='linear'),
    )

    # Display the interactive plot
    fig.show()


def create_weakly_change_plot(values):
    avg_prices, percentage_changes = calculate_weekly_changes(values)
    percentage_changes.insert(0, 0)

    # Create a plot for average prices with percentage change annotations
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(avg_prices) + 1), avg_prices, marker='o', linestyle='-', color='b')
    plt.xlabel('Week')
    plt.ylabel('Average Price')
    plt.title('Average Prices for Each Week')

    # Add annotations for percentage changes
    for i, change in enumerate(percentage_changes):
        if change >= 0:
            change_str = f'+{change:.2f}%'
            color = 'green'
        else:
            change_str = f'{change:.2f}%'
            color = 'red'

        plt.annotate(change_str, (i + 1, avg_prices[i]), textcoords="offset points", xytext=(0, 10),
                     ha='center', fontsize=9, color=color)

    plt.grid(True)
    plt.tight_layout()
    plt.show()



def calculate_weekly_operation_price_for_quality(operation_data, skin_quality, wear):
    weakly_prices = []
    earliest_date, latest_date = calculate_earliest_and_latest_date(operation_data)

    f = None
    if wear is not None:
        f = [item for item in operation_data if item[2] == wear]
    else:
        f = operation_data.copy()

    filtered_data = [item for item in f if item[3] == skin_quality]

    for skin in filtered_data:
        json_data = json.loads(skin[8])
        dates, values = extract_data_from_json(json_data)
        tmp = create_weekly_price_dictionary(earliest_date, latest_date, dates, values)
        expand_weekly_averages(tmp)
        weakly_prices.append(tmp)

    res = None
    for dictionary in weakly_prices:
        val_list = convert_dict_to_values_list(dictionary)
        if res is None:
            res = val_list.copy()
        else:
            res = np.add(res, val_list)

    return np.array(res) / len(weakly_prices)

def filter_data_skin_quality(operation_data, skin_qualities):
    if skin_qualities is not None:
        return [item for item in operation_data if item[3] in skin_qualities]
    else:
        return operation_data.copy()


def filter_data_skin_souvenir(operation_data, option=0):
    return [item for item in operation_data if item[4] == option]

def filter_data_skin_wears(operation_data, wears):
    if wears is not None:
        return [item for item in operation_data if item[2] in wears]
    else:
        return operation_data.copy()

def fiter_data_skin_name(operation_data, weapon, name):
    if name is not None:
        name = [item for item in operation_data if name in item[1]]
        if len(name) != 0:
            if weapon is not None:
                return [item for item in name if weapon in item[1]]
            return name
        return []
    elif weapon is not None:
        return [item for item in operation_data if weapon in item[1]]
    else:
        return []


def calculate_operation_price_changes(operation_name):
    print("XD")



def shorten_data(data, number_of_data):
    if len(data) < number_of_data:
        return data
    elif number_of_data <= 0:
        return []
    else:
        return data[:number_of_data]


def znajdz_przedzialy_wzrostowe_i_spadkowe(dane, prog_spadku=0.1, min_dlugosc_przedzialu=3):
    przedzialy_wzrostowe = []
    przedzialy_spadkowe = []
    aktualny_przedzial = None
    dlugosc_aktualnego_przedzialu = 0
    poczatkowa_cena = None

    for tydzien, cena in enumerate(dane):
        if aktualny_przedzial is None:
            if tydzien == 0:
                poczatkowa_cena = cena
            aktualny_przedzial = tydzien
            dlugosc_aktualnego_przedzialu = 1
        else:
            zmiana_procentowa = (cena - poczatkowa_cena) / poczatkowa_cena

            if zmiana_procentowa <= -prog_spadku:
                if dlugosc_aktualnego_przedzialu >= min_dlugosc_przedzialu:
                    przedzialy_spadkowe.append((aktualny_przedzial + 1, tydzien + 1))
                aktualny_przedzial = None
                dlugosc_aktualnego_przedzialu = 0
            elif zmiana_procentowa >= prog_spadku:
                if dlugosc_aktualnego_przedzialu >= min_dlugosc_przedzialu:
                    przedzialy_wzrostowe.append((aktualny_przedzial + 1, tydzien + 1))
                aktualny_przedzial = None
                dlugosc_aktualnego_przedzialu = 0
            else:
                dlugosc_aktualnego_przedzialu += 1

    # Łączenie spadkowych przedziałów, które się łączą
    przedzialy_spadkowe_polaczone = []
    if przedzialy_spadkowe:
        aktualny_przedzial_polaczony = przedzialy_spadkowe[0]
        for przedzial in przedzialy_spadkowe[1:]:
            if przedzial[0] == aktualny_przedzial_polaczony[1] + 1:
                aktualny_przedzial_polaczony = (aktualny_przedzial_polaczony[0], przedzial[1])
            else:
                przedzialy_spadkowe_polaczone.append(aktualny_przedzial_polaczony)
                aktualny_przedzial_polaczony = przedzial
        przedzialy_spadkowe_polaczone.append(aktualny_przedzial_polaczony)

    # Łączenie wzrostowych przedziałów, które się łączą
    przedzialy_wzrostowe_polaczone = []
    if przedzialy_wzrostowe:
        aktualny_przedzial_polaczony = przedzialy_wzrostowe[0]
        for przedzial in przedzialy_wzrostowe[1:]:
            if przedzial[0] == aktualny_przedzial_polaczony[1] + 1:
                aktualny_przedzial_polaczony = (aktualny_przedzial_polaczony[0], przedzial[1])
            else:
                przedzialy_wzrostowe_polaczone.append(aktualny_przedzial_polaczony)
                aktualny_przedzial_polaczony = przedzial
        przedzialy_wzrostowe_polaczone.append(aktualny_przedzial_polaczony)

    return przedzialy_wzrostowe_polaczone, przedzialy_spadkowe_polaczone



def find_significant_increase(prices, threshold_percentage):
    for i in range(len(prices) - 1):
        price = prices[i]
        next_price = prices[i + 1]
        increase_percentage = ((next_price - price) / price) * 100

        if increase_percentage >= threshold_percentage:
            return i, i + 1

    return None

def merge_intervals(intervals):
    merged_intervals = []
    if len(intervals) == 0:
        return merged_intervals

    intervals.sort()
    current_interval = intervals[0]

    for interval in intervals[1:]:
        if interval[0] <= current_interval[1]:
            current_interval = (current_interval[0], max(current_interval[1], interval[1]))
        else:
            merged_intervals.append(current_interval)
            current_interval = interval

    merged_intervals.append(current_interval)
    return merged_intervals


def find_increase_intervals(prices, threshold_percentage=0):
    increase_intervals = []
    start_index = 0
    for i in range(1, len(prices)):
        increase_percentage = ((prices[i] - prices[start_index]) / prices[start_index]) * 100
        if increase_percentage >= threshold_percentage:
            increase_intervals.append((start_index, i))
        start_index = i

    return merge_intervals(increase_intervals)


def find_decreasing_intervals(prices, threshold_percentage=0):
    decreasing_intervals = []
    start_index = 0
    for i in range(1, len(prices)):
        increase_percentage = ((prices[i] - prices[start_index]) / prices[start_index]) * 100
        if increase_percentage <= threshold_percentage:
            decreasing_intervals.append((start_index, i))
        start_index = i
    return merge_intervals(decreasing_intervals)


def main():
    name = input("Poodaj nazwe: ")
    data = dbHelper.get_skin_from_base(name, "Minimal Wear", False, False)
    json_data = json.loads(data)
    print(data)
    dates, values = extract_data_from_json(json_data)
    # create_price_plot(dates,values)
    create_weakly_change_plot(values)
    # Extract dates and values into separate lists



def cutoff_data(data, new_len):
    return data[:new_len]

def calculate_weekly_price(collection_name, args):
    qualities = argumentsHelper.extract_qualities_args(args)
    wears = argumentsHelper.extract_wears_args(args)
    collection_data = dbHelper.get_skins_from_collection(collection_name)
    collection_data = filter_data_skin_quality(collection_data, qualities)
    collection_data = filter_data_skin_wears(collection_data, wears)
    collection_data = filter_data_skin_souvenir(collection_data)
    weekly_prices = calculate_weekly_operation_price(collection_data)
    return weekly_prices


#poprawne
def compere_collections(collection1_name, collection2_name, args):

    collection1_prices = calculate_weekly_price(collection1_name, args)
    collection2_prices = calculate_weekly_price(collection2_name, args)

    if len(collection1_prices) > len(collection2_prices):
        collection1_prices = cutoff_data(collection1_prices, len(collection2_prices))
    else:
        collection2_prices = cutoff_data(collection2_prices, len(collection1_prices))

    weeks = [x for x in range(len(collection1_prices))]

    data = {
        "collection1": collection1_prices,
        "collection2": collection2_prices,
        "weeks": weeks
    }
    json_data = json.dumps(data)
    return json_data


def skin_weekly_prices(selected_collection, option, args):

    if selected_collection is None:
        return None

    qualities = argumentsHelper.extract_qualities_args(args)
    wears = argumentsHelper.extract_wears_args(args)
    weekly_prices = None
    weeks_numbers = None


    #todo przemyślec jeszcze filtrowanie
    if option == 'all':
        collection_data = dbHelper.get_skins_from_collection(selected_collection)
        weekly_prices = calculate_weekly_operation_price(collection_data)
        weeks_numbers = [x for x in range(len(weekly_prices))]

    if option == 'skin':
        name = argumentsHelper.extract_name(args)
        weapon = argumentsHelper.extract_weapon(args)
        collection_data = dbHelper.get_skins_from_collection(selected_collection)
        skin = fiter_data_skin_name(collection_data, weapon, name)
        skin_filtered = filter_data_skin_wears(skin, wears)
        if len(skin_filtered) > 0:
            weekly_prices = calculate_weekly_operation_price(skin_filtered)
            weeks_numbers = [x for x in range(len(weekly_prices))]
        else:
            weekly_prices = None
            weeks_numbers = None

    if option == 'quality':
        collection_data = dbHelper.get_skins_from_collection(selected_collection)
        filtered_data_color = filter_data_skin_quality(collection_data, qualities)
        filtered_data_wears = filter_data_skin_wears(filtered_data_color, wears)
        weekly_prices = calculate_weekly_operation_price(filtered_data_wears)
        weeks_numbers = [x for x in range(len(weekly_prices))]

    data = {
        "weekly_prices": weekly_prices,
        "weeks_numbers": weeks_numbers,
    }
    json_data = json.dumps(data)
    return json_data


if __name__ == '__main__':
    main()
    # Convert lists to numpy arrays
