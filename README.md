# Illinois Public Libraries' Internet Access

## I. Project Background

The Internet Equity Initiative (IEI) works toward realizing equitable, resilient, and sustainable Internet solutions that benefit all communities. IEI focuses in  3 areas: data measurement and analysis, connectivity evaluation models, and social infrastructure investments. In partnership with the State of Illinois, the IEI aimed to assess and evaluate Internet access at public anchor institutions in Illinois (schools, healthcare organizations, government buildings, libraries).

## II. Project Goals

The purpose of this project was to spatially identify Internet access at all public libraries in Illinois, through an interactive open broadband map. The IEI used this information and map to understand broadband access at libraries and identify any areas of concern or lack of access throughout the state. Highlighting these areas to local government officials will help address inequity in vital Internet access in Illinois's communities.

## III. Analytics Process

The process can be summarized in five major steps:

### 1. Identify and Geocode Illinois's Libraries
Given that the directory of public libraries in Illinois was not available in a tabular form, a web scraper was built to retrieve the library names and addresses. Once the addresses were in a clean format, the [Google's Geocoding API](https://developers.google.com/maps/documentation/geocoding/overview) was used to obtain the libraries' point location on Earth (latitude/longitude). The **library dataset** contains the name, address, and location of 781 public libraries.

### 2. Add Public Library Internet Survey to the Library Dataset
The [Public Library Internet Survey](https://www.illinoisheartland.org/news/content/illinois-public-library-internet-survey-info-page) is a statewide effort to retrieve data about broadband access and its usage in public libraries. This survey contains information about internet access, connectivity speeds, and so on. Following the same approach as in step 1, the addresses of this dataset were passed into Google's Geocoding API to obtain their point location. Then, a join was performed between the library dataset and the survey dataset to add survey connectivity variables to the library dataset. After cleaning, 47.5% of the observations were assigned with connectivity variables. 

### 3. Spatial Join between Library Dataset and ACS Dataset
The American Community Survey (ACS) has data on [how households access the internet](https://www.census.gov/acs/www/about/why-we-ask-each-question/computer/). This data is used as a proxy variable to measure internet access for public libraries. The assumption here is that if a household is located in the same census tract where a library is present and the household doesn’t have access to internet service, it is likely that the library doesn’t have access either.

To add data from the ACS to the library dataset a spatial join operation was performed. Each library was assigned to a specific census tract based on the library coordinates and the polygon (*i.e.*, census tract shape) coordinates of the census tract. In this sense, a library will have ACS data depending on the census tract it is assigned.

### 4. Spatial Join between Library Dataset and FCC Dataset
The Federal Communications Commission (FCC) has data on internet service providers and advertized speeds. An example of these can be found in their [broadband map](https://broadbandmap.fcc.gov/home). Using a similar approach as in step 4, a spatial join is implemented to add data to a library that captures the average number of providers and advertised download/upload speeds in an area.

### 5. Visualization
The vizualization consists of an interactive map application that shows information on internet access for public libraries in Illinois. An example of an R Shiny App can be found [by clicking here](https://ssegovba.shinyapps.io/broadband_access_il_app/).

## IV. Repository Structure

### utils
Project python code.

### notebooks
Contains short, clean notebooks to demonstrate analysis.

### data
Contains details of acquiring all raw data used in repository.

### shiny-code
Contains the soruce code of the Shiny App.