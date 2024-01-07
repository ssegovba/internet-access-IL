## Scripts description

This file contains information about what is done in each script

* `acs_pull.py`: This script retrieves American Community Survey data related to household internet access from the Census API. To ensure the security of your API key, it's recommended to create a separate .py file that stores this sensitive information as a constant. Once you run the script, it will generate two CSV files: 1) "acs_internet_use.csv," which contains data at the census tract level, and 2)"acs_internet_use_block.csv," which contains data at the block group level.

* `agg_fcc_data.py`: This code uses the broadband data from the FCC to create an aggregated data structure with broadband data by hexagon. The aggregated data is exported as a csv file to the `data/` folder.

* `clean_lib_data.py`: This code cleans the data from the libraries scraped in `scraping_libraries.py`. The output is stored in the /data folder as a json file (`clean_lib_data_xxx.json`). If the code is run in the console, it will ask for library type code. The codes can be found at the beginning of the file.

* `data_merge.py`: This script takes data from the ACS, FCC, and libraries locations to create a single merged geodataframe that contains data on libraries's broadband access.

* `fcc_pull.py`: This script retrives data from the FCC's US National Broadband map for Illinois, using an API from Virginia Tech. To ensure the security of your API key, it's recommended to create a separate .py file that stores this sensitive information as a constant. Once you run the script, a csv file will be stored in the path of your choosing.

* `geocoding_libs.py`: This code takes the output from `clean_lib_data.py`, connects to Google's Geocoding API, takes the libraries addresses, and retrieves their point location on Earth (latitude/longitude). The output is stored in the /data folder as a CSV file (`geocoded_lib_data_xxx.csv`).

*`load_data.py`: This script loads and handles data from the ACS, FCC, libraries locations, and Census Tract boundaries, and returns them as dataframes.

* `scraping_libraries.py`: This code scrapes all the libraries names and addresses from the [Library & Learning webpage](https://librarylearning.org/directory). The output is stored in the /data folder as a json file (`lib_data_xxx.json`). If the code is run in the console, it will ask for library type code. The codes can be found at the beginning of the file.