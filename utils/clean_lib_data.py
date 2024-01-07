"""
This script cleans the data from the libraries scraped from L2 website
"""
import json

# Define initial arguments
LIB_CODES = {
    "All": "all",
    "123": "academic",
    "124": "public",
    "125": "school",
    "126": "special",
    "963": "state_lib",
    "964": "regional_system",
    "965": "catalog_consortium",
}


# Define functions that load the data and clean the records
def load_data(lib_type):
    """
    Load the data to be cleaned

    Input:
        lib_type (str): a str containing the code of the type of libraries

    Output:
        data (dict): dictionary with libraries names as keys and addresses as
            values
    """
    file_name = "../data/lib_data_" + LIB_CODES[lib_type] + ".json"
    with open(file_name) as file:
        data = json.load(file)

    return data


def clean_library_record(addr):
    """
    Takes an library's address(es) and return a clean version of it
    Input:
        addr_lst (lst): a list containing all scraped addresses for a library

    Output:
        clean_addr (lst): a list of strings with the clean addresses
    """
    parts = addr.split("\n")
    if len(parts) == 2:
        return " ".join(parts)
    elif len(parts) == 3:
        return " ".join([parts[0], parts[2]])
    else:
        return addr


def clean_dataset(data_dict):
    """ """
    clean_data = {}

    for lib in data_dict:
        lib_addrs = data_dict[lib]
        for addr in lib_addrs:
            if lib not in clean_data:
                clean_data[lib] = [clean_library_record(addr)]
            else:
                clean_data[lib].append(clean_library_record(addr))

    return clean_data


if __name__ == "__main__":
    # Initial statements
    print("Enter the library type code to clean corresponsing dataset:")
    lib_code = input()

    # If digit string represents an integer, cleans the data
    if lib_code.isdigit() and lib_code in LIB_CODES:
        ini_data = load_data(lib_code)
        new_data = clean_dataset(ini_data)

        # Exports the dataset
        file_name = "../data/clean_lib_data_" + LIB_CODES[lib_code] + ".json"
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)
    else:
        print("Please enter a valid library code.")
