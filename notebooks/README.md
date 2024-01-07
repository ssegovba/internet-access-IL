### Notebook directory

This file contains information about what is done in each notebook

* `libs_survey_data.ipynb`: This notebook explores and cleans the data from the survey on broadband access for public libraries. The survey data is used along with the geocoded data from the libraries (`geolib_df`) obtained from `utils/geocoding_libs.py`. The resulting dataset from this process is a library dataset that contains the name, address and geolocation of the libraries, as well as data on broadband access (`data/lib_data_plot.csv`).
* `viz_example.ipynb`: This notebook has an example of the desired visualization using `folium`. The final version is accesible in the main `README.md` file of the repository.