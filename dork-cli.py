#!/usr/bin/env python
import urllib2
import urllib
import json
import sys

num_results = 50
extensions = ['asp', 'aspx', 'cfm', 'cgi', 'jsp', 'php', 'phtm', 'phtml', 'shtm', 'shtml']

data = {}
data['key'] = 'YOUR_KEY_HERE'
data['cx'] = 'YOUR_ENGINE_ID_HERE'
data['q'] = 'filetype:' + ' OR filetype:'.join(extensions) + ' ' + ' '.join(sys.argv[1:])
data['num'] = 10
data['start'] = 1

while data['start'] + data['num'] <= num_results + 1:
    url = 'https://www.googleapis.com/customsearch/v1?'+ urllib.urlencode(data)
    response = json.load(urllib2.urlopen(url))
    for item in response['items']:
        print item['link']
    data['start'] += data['num']

