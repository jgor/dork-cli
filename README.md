dork-cli
========

Command-line utility for finding dynamic webpages within a Google Custom Search Engine (CSE) using Google dorks.

## Setup ##
In order to use this program you need to configure at a minimum two settings in dork-cli.py: a Google API key and a custom search engine id. Additionally you can configure the number of search results returned per run as well as the list of dynamic file extensions searched.

Custom Search Engine:
* Create a custom search engine via https://www.google.com/cse/
* Add your desired domain(s) under "Sites to search"
* Set the engine id (the cx value in your CSE's url) in dork-cli.py

API key:
* Open the Google API console at https://code.google.com/apis/console
* Enable the Custom Search API via APIs & auth > APIs
* Create a new API key via APIs & auth > Credentials > Create new Key
* Select "Browser key", leave HTTP Referer blank and click Create
* Set the API key in dork-cli.py

## Usage ##
./dork-cli.py [additional search terms / dorks]

example: ./dork-cli.py inurl:login intitle:admin

## API Limitations ##
The free Google API limits you to 100 searches per day, with a maximum of 10 results per search. This means if you configure dork-cli.py to return 100 results, it will issue 10 queries (1/10th of your daily limit) each time it is run. You have the option to pay for additional searches via the Google API console.

