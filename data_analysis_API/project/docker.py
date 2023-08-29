from flask import Flask, request
import dbHelper
import json

import skinAnalysys

app = Flask(__name__)


@app.route('/')
def hello():
    return "hello"



@app.route('/collections')
def get_collection():
    collections = dbHelper.get_collections_names()
    return json.dumps(collections)


@app.route('/skin_weekly_prices', methods=['POST'])
def get_skin_weekly_prices():
    data = request.json

    selected_collection = data.get('selected_collection', '')
    option = data.get('option', None)
    args = data.get('args', None)
    return skinAnalysys.skin_weekly_prices(selected_collection, option, args)


@app.route('/increase_interval', methods=['POST'])
def get_increase_intervals():
    skin_data = get_skin_weekly_prices()
    prices = json.loads(skin_data)['weekly_prices']
    intervals = skinAnalysys.find_increase_intervals(prices, threshold_percentage=-2.5)
    data = {
        "weekly_prices": prices,
        "intervals": intervals,
    }
    json_data = json.dumps(data)
    return json_data


@app.route('/decrease_interval', methods=['POST'])
def get_decrease_intervals():
    skin_data = get_skin_weekly_prices()
    prices = json.loads(skin_data)['weekly_prices']
    intervals = skinAnalysys.find_decreasing_intervals(prices, threshold_percentage=-2.5)
    data = {
        "weekly_prices": prices,
        "intervals": intervals,
    }
    json_data = json.dumps(data)
    return json_data



@app.route('/compere_collections', methods=['POST'])
def compere_collection_prices():
    data = request.json
    collection1_name = data.get('collection1', '')
    collection2_name = data.get('collection2', '')
    args = data.get('args', '')
    return skinAnalysys.compere_collections(collection1_name,collection2_name, args)


@app.route('/skins', methods=['POST'])
def get_skins_names():
    data = request.json
    collection_name = data.get('collection', '')
    skins = dbHelper.get_skins_names_from_collection(collection_name)
    return json.dumps(skins)













if __name__ == '__main__':
    print("Startuje")
    app.run(host='0.0.0.0', port=5000)
    print("Dzialam")