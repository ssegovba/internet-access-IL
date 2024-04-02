rm(list=ls())
library(shiny)
library(sf)
library(ggplot2)
library(leaflet)
library(leaflet.extras)
library(bslib)
library(fmsb)
library(DT)

# Load data
acs_data <- read_sf("data/acs_data/acs_data.shp")
lib_data <- read_sf("data/lib_data/lib_data.shp")
fcc_data <- read.csv("data/fcc_data/fcc_data_agg.csv")
lib_data <- lib_data[order(lib_data$lib_name),]
lib_data_num <- as.data.frame(lib_data)
lib_data_num <- subset(lib_data_num, select = -c(geometry))
non_lib_acs <- acs_data[!acs_data$GEOID20 %in% unique(lib_data$GEOID20),]

# Define color palette
pal <- colorNumeric(palette = "RdPu",
                    domain = c(acs_data$share_broa,
                               acs_data$share_cell,
                               acs_data$share_sate,
                               acs_data$share_no_i)
)

# Define UI
ui <- fluidPage(
    # Define theme
    theme = bs_theme(bootswatch = "litera"),
    
    # Define main title
    titlePanel(tags$h1("Broadband Access for Public Libraries in IL - by Santiago Segovia")),
    
    # Define the structure for inputs and outputs
    navlistPanel(
        HTML("<h4>Visualization</h4>"),
        tabPanel("Broadband Access",
                 fluidRow(
                     column(6, selectInput("choroplethInput", "Select Chroropleth Layer:",
                                           choices = c("Broadband", "Cellular", "Satellite", "No Internet")))
                 ),
                 HTML("<p>This section uses data from the 2022 American Community Survey (ACS) to visualize broadband access across various census tracts in IL. \
                      The layers represent the share of households at the census tract level that have access to internet based on four categories: broadband, cellular data, satellite and internet. The \
                      markers correspond to the location of public libraries and the popup has info on households' access data for the census tract a library falls into.<br><br> \
                      <strong>How to understand the data</strong>: if a library is located in an area where a higher share of households don't have internet access, is more likely the library don't have access either.</p>"),
                 leafletOutput("map", height = "60vh")
        ),
        HTML("<br>"),
        HTML("<h4>In-Depth Statistics</h4>"),
        tabPanel("Detailed Analysis",
                 fluidRow(
                     column(6, selectInput("acsInput", "Select ACS variable:",
                                           choices = c("Broadband", "Cellular", "Satellite", "No Internet"))),
                     column(6,selectInput("libraryInput", "Select Library:",
                                          choices = unique(lib_data$lib_name)))
                 ),
                 HTML("<p>This section uses data from the ACS and FCC to create two types of graphs. The <strong>histogram</strong> shows the distribution of types of internet access for census tracts where libraries are present or not. An individual \
                      library can be selected to display its value and locate it in the distribution. The <strong>spider chart</strong> shows data on histogram shows how that individual library is compared to the average.</p>"),
                 plotOutput("histogram"),
                 textOutput("lib_info"),
                 textOutput("spider_info"),
                 plotOutput("spiderChart")
        ),
        HTML("<br>"),
        HTML("<h4>Data</h4>"),
        tabPanel("Libraries Locations",
                 HTML("<h4>Description</h4><br>"),
                 HTML("<p>The data from the locations of public libraries in Illinois comes from the <a href=\"https://librarylearning.org/directory\"> Library Directory and Learning Calendar</a>.\
                      Since no geographical data exist, the website was scraped to retrieve the libraries' names and addresses. \
                      Once the addresses were retrieved, we use Google's Georeferencing API to obtain each library's latitude/longitude pair.<br><br>\
                      The final structure is the following:</p>"),
                 dataTableOutput("table_lib")
        ),
        tabPanel("ACS Data",
                 HTML("<h4>Description</h4><br>"),
                 HTML("<p>The 2022 American Community Survey (ACS) data was obtained through the website's API.\
                      This corresponds to the<a href=\"https://www.census.gov/acs/www/about/why-we-ask-each-question/computer/\"> household's access to broadband services</a>, which \
                      serves as a proxy variable to determine the libraries' access to the internet. The data is obtained at the census tract level, so we \
                      also use data of their boundaries to create the choropleth layers.<br><br>The final structure is the following:</p>"),
                 dataTableOutput("table_acs")
        ),
        tabPanel("FCC Data",
                 HTML("<h4>Description</h4><br>"),
                 HTML("<p>The data from the Federal Communications Commission (FCC) comes from the <a href=\"https://broadbandmap.fcc.gov/home\"> US National Broadband map</a>. This \
                      map provides information about the internet services available to individual locations across the country. However, libraries are not included in that map. To construct \
                      a proxy for this, we use the hexagonal hierarchical geospatial methodology (H3) to calculate the average number of providers, advertised download speeds, \
                      and advertised upload speeds per hexagon. Then, this data is added to the libraries dataset depending on which hexagon they fall into.<br><br> \
                      The final structure for the FCC dataset is the following:</p>"),
                 dataTableOutput("table_fcc")
        )
    )
)


# Define server logic
server <- function(input, output) {
    # Reactive expression to create the map based on the input
    mapData <- reactive({
        # Add layers based on the selected input
        if (input$choroplethInput == "Broadband") {
            m <- leaflet(acs_data) %>%
                addTiles() %>%
                addPolygons(
                fillColor = ~pal(share_broa),
                weight = 1,
                opacity = 1,
                color = "white",
                dashArray = "3",
                fillOpacity = 0.7,
                highlight = highlightOptions(
                    weight = 3,
                    color = "grey",
                    dashArray = "",
                    fillOpacity = 0.7,
                    bringToFront = TRUE),
                label = ~paste0(round(share_broa,2), "%"),
                labelOptions = labelOptions(
                    style = list("font-weight" = "normal", padding = "3px 8px"),
                    textsize = "15px",
                    direction = "auto"),
                group = "Broadband"
                ) %>%
                addLegend(
                    pal = pal,
                    values = ~share_broa,
                    opacity = 0.7,
                    title = "Broadband (%)",
                    position = "bottomright",
                    group = "Obesity")
        } else if (input$choroplethInput == "Cellular") {
            m <- leaflet(acs_data) %>%
                addTiles() %>%
                addPolygons(
                    fillColor = ~pal(share_cell),
                    weight = 1,
                    opacity = 1,
                    color = "white",
                    dashArray = "3",
                    fillOpacity = 0.7,
                    highlight = highlightOptions(
                        weight = 3,
                        color = "grey",
                        dashArray = "",
                        fillOpacity = 0.7,
                        bringToFront = TRUE),
                    label = ~paste0(round(share_cell,2), "%"),
                    labelOptions = labelOptions(
                        style = list("font-weight" = "normal", padding = "3px 8px"),
                        textsize = "15px",
                        direction = "auto"),
                    group = "Cellular"
                    ) %>%
                addLegend(
                    pal = pal,
                    values = ~share_cell,
                    opacity = 0.7,
                    title = "Cellular (%)",
                    position = "bottomright",
                    group = "Cellular")
        } else if (input$choroplethInput == "Satellite") {
            m <- leaflet(acs_data) %>%
                addTiles() %>%
                addPolygons(
                    fillColor = ~pal(share_sate),
                    weight = 1,
                    opacity = 1,
                    color = "white",
                    dashArray = "3",
                    fillOpacity = 0.7,
                    highlight = highlightOptions(
                        weight = 3,
                        color = "grey",
                        dashArray = "",
                        fillOpacity = 0.7,
                        bringToFront = TRUE),
                    label = ~paste0(round(share_sate,2), "%"),
                    labelOptions = labelOptions(
                        style = list("font-weight" = "normal", padding = "3px 8px"),
                        textsize = "15px",
                        direction = "auto"),
                    group = "Satellite"
                    ) %>%
                addLegend(
                    pal = pal,
                    values = ~share_sate,
                    opacity = 0.7,
                    title = "Satellite (%)",
                    position = "bottomright",
                    group = "Satellite")
        } else if (input$choroplethInput == "No Internet") {
            m <- leaflet(acs_data) %>%
                addTiles() %>%
                addPolygons(
                    fillColor = ~pal(share_no_i),
                    weight = 1,
                    opacity = 1,
                    color = "white",
                    dashArray = "3",
                    fillOpacity = 0.7,
                    highlight = highlightOptions(
                        weight = 3,
                        color = "grey",
                        dashArray = "",
                        fillOpacity = 0.7,
                        bringToFront = TRUE),
                    label = ~paste0(round(share_no_i,2), "%"),
                    labelOptions = labelOptions(
                        style = list("font-weight" = "normal", padding = "3px 8px"),
                        textsize = "15px",
                        direction = "auto"),
                    group = "No Internet"
                    ) %>%
                addLegend(
                    pal = pal,
                    values = ~share_no_i,
                    opacity = 0.7,
                    title = "No Internet (%)",
                    position = "bottomright",
                    group = "No Internet")
        }
        
        # Add other common layers like markers
        m <- m %>%
            addMarkers(data = lib_data,
                       lng = ~longitude,
                       lat = ~latitude,
                       popup = ~paste0(
                           "<strong>Library Name:</strong>", lib_name, "<br>",
                           "<strong>Share Broadband (%):</strong>", round(share_broa,2), "<br>",
                           "<strong>Share Cellular (%):</strong>", round(share_cell,2), "<br>",
                           "<strong>Share Satellite (%):</strong>", round(share_sate,2), "<br>",
                           "<strong>Share No Internet (%):</strong>", round(share_no_i,2), "<br>"),
                       clusterOptions = markerClusterOptions())
        
        # Return the map object
        m
    })
    
    # Render the map
    output$map <- renderLeaflet({
        mapData()
    })
    
    # Reactive expression for the histogram
    histogramData <- reactive({
        selected_var <- switch(input$acsInput,
                               "Broadband" = "share_broa",
                               "Cellular" = "share_cell",
                               "Satellite" = "share_sate",
                               "No Internet" = "share_no_i")

        # Selecting only the necessary columns
        lib_data_selected <- lib_data[, c(selected_var)]
        lib_data_selected$type <- "Library"
        
        non_lib_data_selected <- non_lib_acs[, c(selected_var)]
        non_lib_data_selected$type <- "Non-Library"
        
        # Combining the datasets
        combined_data <- rbind(lib_data_selected, non_lib_data_selected)
        
        return(list("data" = combined_data, "var" = selected_var))
    })
    
    # Render the histogram
    output$histogram <- renderPlot({
        hist_data <- histogramData()
        if (is.null(hist_data)) {
            return(NULL)
        }
        
        data <- hist_data$data
        var <- hist_data$var
        
        ggplot(data, aes_string(x = var, fill = "type")) +
            geom_density(alpha = 0.5) +  # Adjust alpha for transparency
            labs(title = paste("Density Plot of", input$acsInput),
                 x = paste("Share of households with internet category:",input$acsInput),
                 y = "Density") +
            scale_fill_manual(values = c("Library" = "lightblue", "Non-Library" = "lightgreen"),
                              name = "Type") +
            theme_minimal() +
            theme(plot.title = element_text(size= 20, hjust = 0.5, face = "bold"),
                  legend.title = element_text(size = 15, face = "bold"),
                  legend.text = element_text(size = 12))
    })
    
    # Render the name of the selected library and its value
    output$lib_info <- renderText({
        selected_library <- lib_data_num[lib_data_num$lib_name == input$libraryInput,]
        if (input$acsInput == "Broadband") var_text <- "share_broa"
        if (input$acsInput == "Cellular") var_text <- "share_cell"
        if (input$acsInput == "Satellite") var_text <- "share_sate"
        if (input$acsInput == "No Internet") var_text <- "share_no_i"
        paste0("The selected library's value for this variable is ", round(selected_library[var_text],2),"%.")
    })
    
    # Text for the spider chart
    output$spider_info <- renderText({
        paste0("When compared to the average value of all the other libraries, the standardized statistics are:")
    })
    
    # Reactive expression for the spider chart data
    spiderData <- reactive({
        selected_library <- lib_data_num[lib_data_num$lib_name == input$libraryInput,]
        if (nrow(selected_library) == 0) {
            return(NULL)
        }
        
        # Calculate average values for all libraries
        avg_values <- as.numeric(colMeans(lib_data_num[,c("share_broa", "share_cell", "share_sate", "share_no_i", "avg_num_pr", "avg_max_do", "avg_max_up")], na.rm=TRUE))
        
        # Normalize the data (if necessary)
        max_values <- c(max(lib_data_num$share_broa), max(lib_data_num$share_cell), max(lib_data_num$share_sate), max(lib_data_num$share_no_i), max(lib_data_num$avg_num_pr), max(lib_data_num$avg_max_do), max(lib_data_num$avg_max_up))
        normalized_selected <- as.numeric(selected_library[,c("share_broa", "share_cell", "share_sate", "share_no_i", "avg_num_pr", "avg_max_do", "avg_max_up")]) / max_values
        normalized_avg <- avg_values / max_values
        
        # Combine selected library data and average data
        data.frame(rbind(normalized_avg, normalized_selected))
    })
    
    # Render the spider chart
    output$spiderChart <- renderPlot({
        spider_data <- spiderData()
        if (is.null(spider_data)) {
            return(NULL)
        }
        radar_data <- rbind(rep(1, 7), rep(0,7), spider_data)
        colnames(radar_data) <- c("Broadband", "Cellular", "Satellite", "No Internet", "Avg Num Providers", "Avg Max Download", "Avg Max Upload")
        colors_in <- c(rgb(0.2,0.5,0.5,0.9), rgb(0.8,0.2,0.2,0.9))
        radarchart(radar_data, axistype = 1,
                   pcol = c(rgb(0.2,0.5,0.5,0.9), rgb(0.8,0.2,0.2,0.9)), 
                   pfcol = c(rgb(0.2,0.5,0.5,0.5), rgb(0.8,0.2,0.2,0.5)), 
                   plwd = c(4, 4), cglcol = "grey", cglty = 1, axislabcol = "grey"
                   )
        legend(x=1.2, y=1.2, legend = c("Average", "Selected"), bty = "n", pch=20 , col=colors_in , text.col = "black", cex=1, pt.cex=3)
        
    }, height = 500)
    
    # Render the table with the data of the libraries
    output$table_lib <- renderDataTable({
        lib_table <- subset(lib_data_num, select = c(lib_name, lib_addres, latitude, longitude))
        datatable(lib_table, extensions = 'Buttons', options = list(dom = 'Bfrtip', 
                                                                   buttons = list('colvis'), 
                                                                   scrollX = TRUE, 
                                                                   pageLength = 20))
    })
    
    # Render the table with the ACS data
    output$table_acs <- renderDataTable({
        acs_table <- subset(acs_data, select = -c(geometry))
        datatable(acs_table, extensions = 'Buttons', options = list(dom = 'Bfrtip', 
                                                                   buttons = list('colvis'), 
                                                                   scrollX = TRUE, 
                                                                   pageLength = 20))
    })
    
    # Render the table with the FCC data
    output$table_fcc <- renderDataTable({
        fcc_table <- subset(fcc_data, select=-c(geometry))
        datatable(fcc_table, extensions = 'Buttons', options = list(dom = 'Bfrtip', 
                                                                   buttons = list('colvis'), 
                                                                   scrollX = TRUE, 
                                                                   pageLength = 20))
    })
}

# Run the application 
shinyApp(ui = ui, server = server)

