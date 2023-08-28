import skinDataConverter


def extract_qualities_args(args):

    if args is None:
        return None
    args_split = args.split("--")
    Q_args = next((element for element in args_split if element.startswith('Q')), None)
    if Q_args is None:
        return None
    qualities_tmp = Q_args[1:].lstrip().split(" ")
    qualities_list = []
    for q in qualities_tmp:
        long_name = skinDataConverter.convert_quality_to_long_name(q)
        if long_name is not None:
            qualities_list.append(long_name)
    return qualities_list


def extract_wears_args(args):
    if args is None:
        return None
    args_split = args.split("--")
    W_args = next((element for element in args_split if element.startswith('W')), None)
    if W_args is None:
        return None
    wears_tmp = W_args[1:].lstrip().split(" ")
    wears = []
    for w in wears_tmp:
        long_name = skinDataConverter.convert_wear_to_long_name(w)
        if long_name is not None:
            wears.append(long_name)
    return wears


def extract_weapon(args):
    if args is None:
        return None
    args_split = args.split("--")
    W_args = next((element for element in args_split if element.startswith('weapon')), None)
    if W_args is None:
        return None
    name = W_args[6:].lstrip().split(" ")
    return name[0]


def extract_name(args):
    if args is None:
        return None
    args_split = args.split("--")
    N_args = next((element for element in args_split if element.startswith('name')), None)
    if N_args is None:
        return None
    name = N_args[4:].lstrip()
    return name