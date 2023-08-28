def convert_wear_to_long_name(short_name):
    dictionary = {
        "fc": "Factory New",
        "mw": "Minimal Wear",
        "ft": "Field-Tested",
        "ww": "Well-Worn",
        "bs": "Battle-Scarred"
    }
    return dictionary.get(short_name.lower(), None)


def convert_quality_to_long_name(short_name):
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
    return dictionary.get(short_name.lower(), None)