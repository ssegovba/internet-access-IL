"""
File that scrapes libraries
The types take several values. The source code shows  but 
"""

import requests
import json
from bs4 import BeautifulSoup

# Last date scrapper was succesfuly executed: Oct. 16, 2023

# Define initial arguments:
BASE_URL = "https://librarylearning.org/directory"
QUERY_URL = "?search=&type={types}&consortium=All&system=All&branch=All"
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


def retrieve_num_pages(url, lib_type):
    """
    Finds the number or pages in the website that need to be scraped.

    Input:
        url (str): a str that contains the base url of the website
        lib_type (str): a str containing the code of the type of libraries, as
            defined in the website's source code.
    Output:
        query_params (lst): a list of the query params that will be used to loop
            over each page in the website
    """
    # Modify URL based on lib_type:
    new_url = (url + QUERY_URL + "&page=0").format(types=lib_type)

    # Load the main page and parse the HTML:
    page = requests.get(new_url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Find all the page queries in the website and keep the last one
    # since it holds the href with the final page:
    pagers = soup.find_all("li", class_="pager__item")
    last_page = pagers[-1]
    pager_content = last_page.find("a", class_="pager__link")
    if pager_content != None:
        pager_link = pager_content["href"]
        pager_number = int(pager_link.split("page=")[-1])

    # Creates the structure with all page query paramenter:
    query_params = []
    for num in range(pager_number + 1):
        query_params.append("&page=" + str(num))

    return query_params


def scrape_one_lib_type(url, lib_type):
    """
    Takes a library type based on the website's classification for them and
    scrapes the names and addresses. These are stored in a dictionary.

    Input:
        url (str): a str that contains the base url of the website
        lib_type (str): a str containing the code of the type of libraries, as
            defined in the website's source code.

    Output:
        lib_data (dict): a dict where the key-value pairs are library names and
        addreses
    """
    # Define structure to save results:
    lib_data = {}

    # Determine the number of pages to scrape:
    query_pages = retrieve_num_pages(url, lib_type)
    num_pages = len(query_pages)

    # Define names of headers to target in table data tag (<td>):
    lib_name_header = "view-field-building-name-table-column"
    lib_addr_header = "view-field-address-table-column"

    # Loops through each page defining the url to scrape:
    for page in range(num_pages):
        new_url = (url + QUERY_URL + query_pages[page]).format(types=lib_type)

        # Load the main page and parse the HTML:
        page = requests.get(new_url, timeout=3)
        soup = BeautifulSoup(page.content, "html.parser")

        # Find all the <td> tags in the website:
        table_rows = soup.find_all("tr")

        # Iterate over each element to retrieve name and address:
        for i, row in enumerate(table_rows):
            if i != 0:  # i == 0 header of the table
                lib_name_td = row.find("td", headers=lib_name_header)
                a_tag = lib_name_td.find("a")
                if a_tag:
                    lib_name = a_tag.get_text(strip=True)
                    if "Bookmobile" in lib_name:
                        lib_name = lib_name_td.get_text(strip=True)
                        lib_name = lib_name.replace("Bookmobile", "")
                    elif "Main Library" in lib_name:
                        lib_name = lib_name_td.get_text(strip=True)
                        lib_name = lib_name.replace("Main Library", "")

                else:
                    lib_name = lib_name_td.get_text(strip=True)

                lib_address_td = row.find("td", headers=lib_addr_header)
                lib_address = lib_address_td.get_text().strip()

                # Assign both to directory:
                if lib_name in lib_data:
                    lib_data[lib_name].append(lib_address)
                else:
                    lib_data[lib_name] = [lib_address]

    return lib_data


if __name__ == "__main__":
    # Initial statements:
    print("Enter the library type code you want to scrape:")
    lib_code = input()

    # input() gives back a str. We check that digit string represent an integer:
    if lib_code.isdigit() and lib_code in LIB_CODES:
        scraped_data = scrape_one_lib_type(BASE_URL, lib_code)

        # Exports the dataset:
        file_name = "../data/lib_data_" + LIB_CODES[lib_code] + ".json"
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(scraped_data, f, ensure_ascii=False, indent=4)
    else:
        print("Please enter a valid library code.")
