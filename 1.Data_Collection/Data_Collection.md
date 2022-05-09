# Data Collection

The first step of our project is data collection. We collected news articles from Argentine newspapers, in Spanish.
We chose newspapers that have an RSS feed separated by categories. The newspapers are:

- Ámbito Financiero
- Clarín
- Diario AR
- Página 12
- Perfil
- Télam (not a newspaper but the Argentine national news agency) 

The categories that we initially chose are:

- Ciencia y tecnología (Science and technology)
- Cultura y Espectáculos (Culture and Shows)
- Deportes (Sports)
- Economía (Economy)
- Internacional (International)
- Policiales (Crime)
- Política (Politics)
- Sociedad (Society)

To obtain our data, we made requests to the RSS webpages, in XML format, and we parsed the results using the library **lxml**. For each article, we saved the header (Título) and a short description (Descripción). We also saved the URL link, the date, the newspaper, and the category. Then we saved the data we obtained in a CSV file.

As the number of news that we collect in one run of the script was small, we make an update script to run multiple times and collect more articles. We collected news from November to March (not at regular intervals).

The files in this folder are:

- news_scraper.py - The initial script.
- updatenews.py - The script to update the CSV file, to collect more news.
- news_data.csv - The CSV file with the data collected.

You will find the detailed code in those scripts.
