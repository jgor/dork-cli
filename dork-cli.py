#!/usr/bin/env python
from __future__ import print_function
try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
    from urllib.error import HTTPError
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen, HTTPError
import json
import sys
import time
import argparse

key = ''
engine = ''
results = 10
sleep = 0
dynamic_extensions = ['asp', 'aspx', 'cfm', 'cgi', 'jsp', 'php', 'phtm', 'phtml', 'shtm', 'shtml']

def main():
    parser = argparse.ArgumentParser(description='Find dynamic pages via Google dorks.')
    parser.add_argument('-e', '--engine', default=engine,
                   help='Google custom search engine id (cx value)')
    parser.add_argument('-k', '--key', default=key,
                   help='Google API key')
    parser.add_argument('-r', '--results', type=int, default=results,
                   help='Maximum number of search results to return')
    parser.add_argument('-s', '--sleep', type=int, default=sleep,
                   help='Seconds to sleep before retry if daily API limit is reached (0=disable)')
    parser.add_argument('terms', metavar='T', nargs='*',
                   help='additional search term')

    args = parser.parse_args()

    if not args.key or not args.engine:
        print("ERROR: [key] and [engine] must be set", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    data = {}
    data['key'] = args.key
    data['cx'] = args.engine
    data['q'] = 'filetype:' + ' OR filetype:'.join(dynamic_extensions) + ' ' + ' '.join(args.terms)
    data['num'] = 10
    data['start'] = 1

    while data['start'] <= args.results:
        if args.results - data['start'] + 1 < data['num']:
            data['num'] = args.results - data['start'] + 1
        url = 'https://www.googleapis.com/customsearch/v1?'+ urlencode(data)
        try:
            response_str = urlopen(url)
            response_str = response_str.read().decode('utf-8')
            response = json.loads(response_str)
        except HTTPError as e:
            response_str = e.read().decode('utf-8')
            response = json.loads(response_str)
            print("error: " + str(response['error']['code']) + " - " + response['error']['message'], file=sys.stderr)
            for error in response['error']['errors']:
                print(error['domain'] + "::" + error['reason'] + "::" + error['message'], file=sys.stderr)
            if args.sleep and "Exceeded" in response['error']['message']:
                print(sys.stderr, "sleeping " + str(args.sleep) + " seconds", file=sys.stderr)
                time.sleep(args.sleep)
                continue
            else:
                sys.exit(1)
        for request in response['queries']['request']:
            if int(request['totalResults']) == 0:
                sys.exit(0)
        for item in response['items']:
            print(item['link'])
        data['start'] += data['num']

if __name__ == "__main__":
    main()

