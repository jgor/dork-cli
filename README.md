dork-cli
========

Command-line utility for finding potentially vulnerable dynamic webpages within a Google Custom Search Engine (CSE) using Google dorks.

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

examples:
<pre>
$ ./dork-cli.py inurl:id
http://www.example.com/its/sla/sla.php?id=1617
http://www.example.com/its/sla/sla.php?id=1593
http://www.example.com/bbucks/index.php?site=5&scode=0&id=720
http://www.example.com/directory/details.aspx?id=33
http://www.example.com/SitePages/VOIP%20ID.aspx
http://www.example.com/personnel_ext.php?id=44
http://www.example.com/its/alerts/event.php?id=7220
http://www.example.com/directory/details.cgi?id=21
</pre>
<pre>
$ ./dork-cli.py inurl:login
https://www.example.com/usher/Login.aspx
https://www.example.com/login/index.php
http://www.example.com/rooms/index.php?option=com_user&view=login&Itemid=8
http://www.example.com/index.php?cmd=login
[...]
</pre>
<pre>
$ ./dork-cli.py intitle:login inurl:admin
https://www.example.com/users/lab/admin/portal.php
https://www.example.com/admin/start/login.aspx?ReturnUrl=%2Fadmin%2Fscheduling%2Faudit%2Fdefault.aspx
http://www.example.com/admin/admin.php
[...]
</pre>

## API Limitations ##
The free Google API limits you to 100 searches per day, with a maximum of 10 results per search. This means if you configure dork-cli.py to return 100 results, it will issue 10 queries (1/10th of your daily limit) each time it is run. You have the option to pay for additional searches via the Google API console.

