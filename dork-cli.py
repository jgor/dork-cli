#!/usr/bin/env python
import urllib2
import urllib
import json
import sys

api_key = 'YOUR_GOOGLE_API_KEY_HERE'
engine_id = 'YOUR_CUSTOM_SEARCH_ENGINE_ID_HERE'
num_results = 30
dynamic_extensions = ['asp', 'aspx', 'cfm', 'cgi', 'jsp', 'php', 'phtm', 'phtml', 'shtm', 'shtml']

data = {}
data['key'] = api_key
data['cx'] = engine_id
data['q'] = 'filetype:' + ' OR filetype:'.join(dynamic_extensions) + ' ' + ' '.join(sys.argv[1:])
data['num'] = 10
data['start'] = 1

while data['start'] <= num_results:
    if num_results - data['start'] + 1 < data['num']:
        data['num'] = num_results - data['start'] + 1
    url = 'https://www.googleapis.com/customsearch/v1?'+ urllib.urlencode(data)
    try:
        response = json.load(urllib2.urlopen(url))
    except urllib2.HTTPError, e:
        response = json.load(e)
        print >> sys.stderr, "error: " + str(response['error']['code']) + " - " + response['error']['message']
        for error in response['error']['errors']:
            print >> sys.stderr, error['domain'] + "::" + error['reason'] + "::" + error['message']
        sys.exit(1)
    for item in response['items']:
        print item['link']
    data['start'] += data['num']

