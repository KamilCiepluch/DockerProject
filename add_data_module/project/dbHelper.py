import json
import requests
import mysql.connector


def get_skin_data_json(weapon, skin_name, wear):
    url = "https://csgobackpack.net/api/GetItemPrice/?currency=USD"
    name = skin_name.strip().replace(" ", "%20")
    wear = wear.strip().replace(" ", "%20")
    url += "&id=" + weapon + "%20|%20" + name + "%20(" + wear + ")"
    url += "&full=1"
    response = requests.get(url)
    return json.dumps(response.json())


def get_st_skin_data_json(weapon, skin_name, wear):
    url = "https://csgobackpack.net/api/GetItemPrice/?currency=USD"
    name = skin_name.strip().replace(" ", "%20")
    wear = wear.strip().replace(" ", "%20")
    url += "&id=" + "StatTrak%20" + weapon + "%20|%20" + name + "%20(" + wear + ")"
    url += "&full=1"
    response = requests.get(url)
    return json.dumps(response.json())


def get_sv_skin_data_json(weapon, skin_name, wear):
    url = "https://csgobackpack.net/api/GetItemPrice/?currency=USD"
    name = skin_name.strip().replace(" ", "%20")
    wear = wear.strip().replace(" ", "%20")
    url += "&id=" + "Souvenir%20" + weapon + "%20|%20" + name + "%20(" + wear + ")"
    url += "&full=1"
    response = requests.get(url)
    return json.dumps(response.json())




def connect_to_database():
    mydb = mysql.connector.connect(
        host="host.docker.internal",  # Nazwa serwisu zdefiniowana w docker-compose.yml
        port=3306,  # Port bazy danych MySQL
        user="root",  # Użytkownik
        password="my-secret-pw",  # Hasło
        database="CSGO_SKINS"  # Nazwa bazy danych
    )
    return mydb


# def connect_to_database():
#     mydb = mysql.connector.connect(
#         host="127.0.0.1",
#         user="root",
#         password="my-secret-pw",
#         database="CSGO_SKINS"
#     )
#     return mydb


def add_skin(skin, wear, quality, stattrack, suvenir, collection, data):
    mydb = connect_to_database()
    mycursor = mydb.cursor()
    args = (skin, wear, quality, stattrack, suvenir, collection, data)
    mycursor.callproc("add_skin", args)
    mydb.commit()

    for result in mycursor.stored_results():
        print(result.fetchall())

    mydb.close()


def add_skin_all_data(weapon, name, quality, collection, can_be_st, can_be_sv):
    number_of_requests = 0

    mydb = connect_to_database()
    mycursor = mydb.cursor()
    skin_name = weapon + ' | ' + name
    wear = ["Factory New", "Minimal Wear", "Field-Tested", "Well-Worn", "Battle-Scarred"]
    for w in wear:
        try:
            mycursor.execute("Select check_skin_exists(%s, %s,%s,%s, %s, %s)",
                             (skin_name, w, quality, False, False, collection))
            result = mycursor.fetchone()[0]
            if result == 0:
                data = get_skin_data_json(weapon, name, w)
                number_of_requests += 1
                add_skin(weapon + " | " + name, w, quality, False, False, collection, data)
        except requests.exceptions.JSONDecodeError:
            continue

    # stattrack
    if can_be_st:
        for w in wear:
            try:
                mycursor.execute("Select check_skin_exists(%s, %s, %s, %s, %s, %s)",
                                 (skin_name, w, quality, True, False, collection))
                result = mycursor.fetchone()[0]
                if result == 0:
                    data2 = get_st_skin_data_json(weapon, name, w)
                    number_of_requests += 1
                    add_skin(weapon + " | " + name, w, quality, True, False, collection, data2)
            except requests.exceptions.JSONDecodeError:
                continue

    # souvenir
    if can_be_sv:
        for w in wear:
            try:

                mycursor.execute("Select check_skin_exists(%s,%s,%s, %s, %s, %s)",  (skin_name, w, quality, False, True, collection))
                result = mycursor.fetchone()[0]
                if result == 0:
                    data3 = get_sv_skin_data_json(weapon, name, w)
                    number_of_requests += 1
                    add_skin(weapon + " | " + name, w, quality, False, True, collection, data3)
            except requests.exceptions.JSONDecodeError:
                continue

    return number_of_requests


def update_data(skin, wear, quality, stattrack, suvenir, collection, data):
    mydb = connect_to_database()
    mycursor = mydb.cursor()
    args = (skin, wear, quality, stattrack, suvenir, collection, data)
    mycursor.callproc("update_skin_data", args)
    mydb.commit()
    mydb.close()


def update_skin_data(weapon, name, quality, collection):
    number_of_requests = 0

    mydb = connect_to_database()
    mycursor = mydb.cursor()
    skin_name = weapon + ' | ' + name
    wear = ["Factory New", "Minimal Wear", "Field-Tested", "Well-Worn", "Battle-Scarred"]
    for w in wear:
        try:
            mycursor.execute("Select check_skin_exists(%s, %s,%s,%s, %s, %s)", (skin_name, w, quality, False, False,collection))
            result = mycursor.fetchone()[0]
            if result != 0:
                data = get_skin_data_json(weapon, name, w)
                number_of_requests += 1
                update_data(weapon + " | " + name, w, quality, False, False, collection, data)
        except requests.exceptions.JSONDecodeError:
            continue

    mycursor.execute("Select check_if_stattrack_exists(%s, %s, %s)", (skin_name, quality, collection))
    can_be_st = mycursor.fetchone()[0]

    mycursor.execute("Select check_if_souvenir_exists(%s, %s, %s)", (skin_name, quality, collection))
    can_be_sv = mycursor.fetchone()[0]

    # stattrack
    if can_be_st != 0:
        for w in wear:
            try:
                mycursor.execute("Select check_skin_exists(%s, %s,%s,%s, %s, %s)",
                                 (skin_name, w, quality, True, False, collection))

                result = mycursor.fetchone()[0]
                if result != 0:
                    data2 = get_st_skin_data_json(weapon, name, w)
                    number_of_requests += 1
                    update_data(weapon + " | " + name, w, quality, True, False, collection, data2)
            except requests.exceptions.JSONDecodeError:
                continue

    # souvenir
    if can_be_sv != 0:
        for w in wear:
            try:
                mycursor.execute("Select check_skin_exists(%s, %s,%s,%s, %s, %s)",
                                 (skin_name, w, quality, False, True, collection))

                result = mycursor.fetchone()[0]
                if result == 0:
                    data3 = get_sv_skin_data_json(weapon, name, w)
                    number_of_requests += 1
                    update_data(weapon + " | " + name, w, quality, False, True, collection, data3)
            except requests.exceptions.JSONDecodeError:
                continue

    return number_of_requests

def get_skin_from_base(skin, wear, st, sv):
    mydb = connect_to_database()
    mycursor = mydb.cursor()
    try:
        mycursor.execute("Select get_skin_data(%s, %s, %s, %s)", (skin, wear, st, sv))
        result = mycursor.fetchone()[0]

        mycursor.close()
        mydb.close()
        return result
    except requests.exceptions.JSONDecodeError:
        return None

def get_skins_from_collection(collection_name):
    mydb = connect_to_database()
    mycursor = mydb.cursor()
    try:
        mycursor.callproc("get_skin_by_collection", (collection_name,))
        result = mycursor.stored_results()
        skins = []
        for res in result:
            for row in res.fetchall():
                skins.append(row)
        mycursor.close()
        mydb.close()
        return skins
    except requests.exceptions.JSONDecodeError:
        return None


def get_collections_names():
    mydb = connect_to_database()
    mycursor = mydb.cursor()
    try:
        mycursor.callproc("get_collections_names", )
        result = mycursor.stored_results()
        collections = []

        for res in result:
            touples = res.fetchall()
            for l in touples:
                collections.append(l[0])
        mycursor.close()
        mydb.close()
        return collections
    except requests.exceptions.JSONDecodeError:
        return None

def add_collection_to_skin(skin, collection):
    mydb = connect_to_database()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT check_skin_name_exists(%s)", (skin,))
    result = mycursor.fetchone()[0]

    if result:
        # Wywołanie procedury update_collection_for_skins
        args = (skin, collection)
        mycursor.callproc("update_collection_for_skins", args)
        mydb.commit()

    mydb.close()


def add_quality_to_skin(skin, quality):
    mydb = connect_to_database()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT check_skin_name_exists(%s)", (skin,))
    result = mycursor.fetchone()[0]

    if result:
        args = (skin, quality)
        mycursor.callproc("update_quality_for_skins", args)
        mydb.commit()

    mydb.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # s ="https://csgobackpack.net/api/GetItemPrice/?currency=USD&id=AK-47%20|%20Asiimov%20(Minimal%20Wear)full=1"
    # s2 ="https://csgobackpack.net/api/GetItemPrice/?currency=USD&id=AK-47%20|%20Asiimov%20(Minimal%20Wear)&time=7&full=1"
    # data = get_skin_data_json("M4A4", "Howl", "Field-Tested")
    # add_skin("M4A4 | Howl", "Field-Tested", False, False, None, data)
    #  data2 = get_st_skin_data_json("AWP", "Dragon Lore", "Field-Tested")
    # add_skin("AWP | Dragon Lore", "Field-Tested", True, False, None, data2)
    # print(data)
    # print(check_skin_existing())

    # add_skin_all("AK-47", "The Empress")
    # add_collection_to_skin("AK-47 | The Empress","Spectrum 2 Case")
    # add_quality_to_skin("AK-47 | The Empress", "Covert")

    add_skin_all_data("★ Gut Knife", "Damascus Steel")

    # while(True):
    #     action = input("Enter action: exit/add: ")
    #     if action == 'exit':
    #         break
    #     if action == 'add':
    #         weapon = input("Enter weapon: ")
    #         skin = input("Enter skin: ")
    #         print("Adding: " + weapon)
    #         add_skin_all(weapon, skin)
    #         print("Adding finished!")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
