import time

import skinNamesLoader as skinLoader
import dbHelper

maxNumberOfRequests = 1000
sleepTime = 3600
number_of_requests = 0


def add_collection_skin(collection, collectionName):
    global number_of_requests
    for quality in collection:
        if quality != 'Rare Special Items':
            for skin in collection[quality]:
                weapon_type, skin_name = skin['name'].split(' | ')
                can_be_st, can_be_sv = skin['can_be_stattrak'], skin['can_be_souvenir'],
                number_of_requests += dbHelper.add_skin_all_data(weapon_type, skin_name, quality, collectionName,
                                                                 can_be_st, can_be_sv)
                print("added skin: ", skin)
                if number_of_requests >= maxNumberOfRequests:
                    print(f"Reached limit of requests! Program will continue after {sleepTime} seconds")
                    time.sleep(sleepTime)
                    if number_of_requests > maxNumberOfRequests:
                        number_of_requests = 0
                        number_of_requests += dbHelper.add_skin_all_data(weapon_type, skin_name, quality,
                                                                         collectionName, can_be_st, can_be_sv)
                    else:
                        number_of_requests = 0

    print(f"Collection: {collectionName} successfully added to base")


def add_skins(collections):
    global number_of_requests
    for collectionName in collections:
        add_collection_skin(collections[collectionName], collectionName)


def add_knifes(collections):
    global number_of_requests
    for collection in collections:
        for quality in collections[collection]:
            if quality == 'Rare Special Items':
                skins = collections[collection][quality]
                for skin in skins:
                    weapon_type, skin_name = skin['name'].split(' | ')
                    can_be_st, can_be_sv = skin['can_be_stattrak'], skin['can_be_souvenir'],

                    # todo chenage collection for json in database and then add more than one collection to items like knife
                    number_of_requests += dbHelper.add_skin_all_data(weapon_type, skin_name, quality, 'Rare Item',
                                                                     can_be_st, can_be_sv)
                    if number_of_requests >= maxNumberOfRequests:
                        print(f"Reached limit of requests! Program will continue after {sleepTime} seconds")
                        time.sleep(sleepTime)
                        if number_of_requests > maxNumberOfRequests:
                            number_of_requests = 0
                            number_of_requests += dbHelper.add_skin_all_data(weapon_type, skin_name, quality,
                                                                             'Rare Item', can_be_st, can_be_sv)
                        else:
                            number_of_requests = 0
            else:
                break
    print(f"Knives from case successfully added to base")


if __name__ == '__main__':
    collections_path = "/app/data/collections"
    cases_path = "/app/data/cases"

    collections = skinLoader.read_json_files(collections_path)
    add_skins(collections)

    collections = skinLoader.read_json_files(cases_path)
    add_skins(collections)
    add_knifes(collections)

    dbHelper.add_skin_all_data('M4A4', 'Howl', 'Contraband', None, True, False)

    print("Program finished adding data")
