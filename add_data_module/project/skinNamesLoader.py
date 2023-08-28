import os
import json



# Function to read JSON files from a directory
def read_json_files_diff(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r',  encoding='utf-8') as json_file:
                try:
                    data = json.load(json_file)
                    collection = data["name"]
                    contentList = data["content"]
                    qualityNames = ['Rare Special Items', 'Covert Skins','Classified Skins', 'Restricted Skins',
                                    'Mil-Spec Skins', 'Industrial Grade Skins', 'Consumer Grade Skins']
                    print(f"{collection}:")
                    for name in qualityNames:
                        skins = contentList[name]
                        print(f"\t{name}:")
                        for skin in skins:
                            print(f"\t\t {skin['name']}")
                except json.JSONDecodeError as e:
                    print(f"Error reading {filename}: {e}")


def read_json_files(directory):
    collections = {}  # Initialize an empty dictionary to store collections and their qualities
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r',  encoding='utf-8') as json_file:
                try:
                    data = json.load(json_file)
                    collection_name = data["name"]
                    content_list = data["content"]
                    quality_names = ['Rare Special Items', 'Covert Skins', 'Classified Skins', 'Restricted Skins',
                                    'Mil-Spec Skins', 'Industrial Grade Skins', 'Consumer Grade Skins']

                    collection_data = collections.setdefault(collection_name, {})  # Get collection data or create if not exists
                    for quality in quality_names:
                        skins = content_list.get(quality, [])  # Get skins for the quality or an empty list if not present
                        if skins:
                            collection_data[quality] = []

                            for skin in skins:
                                skin_info = {
                                    "name": skin['name'],
                                    "can_be_souvenir": skin.get('can_be_souvenir', False),
                                    "can_be_stattrak": skin.get('can_be_stattrak', False)
                                }
                                collection_data[quality].append(skin_info)



                except json.JSONDecodeError as e:
                    print(f"Error reading {filename}: {e}")

    return collections




def get_collections_for_skin(skin_name, collections_data):
    collections_with_skin = []

    for collection, qualities in collections_data.items():
        for quality, skins in qualities.items():
            if any(skin == skin_name for skin in skins):
                collections_with_skin.append(collection)
                break  # Once we find the skin, we don't need to check the rest

    return collections_with_skin


#
# def main():
#     collections_data = read_json_files(directory_path)
#     skin_to_find = "M4A4 | Howl"
#     collections_for_skin = get_collections_for_skin(skin_to_find, collections_data)
#
#     if collections_for_skin:
#         print(f"Skin '{skin_to_find}' can be found in the following collections:")
#         for collection in collections_for_skin:
#             print(collection)
#     else:
#         print(f"Skin '{skin_to_find}' was not found in any collections.")




# Printing the collections and their data
# for collection, qualities in collections_data.items():
#     print(f"{collection}:")
#     for quality, skins in qualities.items():
#         print(f"\t{quality}:")
#         for skin in skins:
#             print(f"\t\t{skin}")