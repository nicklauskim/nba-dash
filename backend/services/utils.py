# Useful miscellaneous helper functions


def rename_columns(api_col_names):
    rename_dict = {}
    for name in api_col_names:
        rename_dict[name] = name.lower()
    return rename_dict


def clean_timestamp(time_string):
    return time_string[:-9]

