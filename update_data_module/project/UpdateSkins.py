import dbHelper
import time
from datetime import datetime


sleepTime = 300
program_sleep_time = 3600

number_of_updated_skins = 0


def update_skins_from_collection(collectionName):
    global number_of_updated_skins
    skins = dbHelper.get_skins_from_collection(collectionName)
    for skin in skins:

        update_date = skin[9]
        date_difference = datetime.now() - update_date
        if date_difference.days >= 1:

            weapon, name = skin[1].split("|")
            weapon, name = weapon.lstrip(), name.lstrip()
            skin, wear, quality, st, sv, coll = skin[1], skin[2], skin[3], skin[4], skin[5], skin[6]
            updated_skins = 0
            while updated_skins == 0:
                try:
                    data = dbHelper.get_skin_data_json(weapon, name, wear)
                    dbHelper.update_data(skin, wear, quality, st, sv, coll, data)
                    updated_skins = 1
                    number_of_updated_skins += 1
                except:
                    print(f"Reached limit of requests! Program will continue after {sleepTime} seconds")
                    time.sleep(sleepTime)


def update_all_collections():
    collections = dbHelper.get_collections_names()
    for collectionName in collections:
        update_skins_from_collection(collectionName)
        print("Updated: ", collectionName)


if __name__ == '__main__':
    while True:
        number_of_updated_skins = 0
        update_all_collections()
        if number_of_updated_skins <= 1:
            time.sleep(program_sleep_time)
