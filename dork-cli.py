#!/usr/bin/env python
from __future__ import print_function
try:
    from urllib.request import urlopen
    from urllib.parse import urlencode,urlparse
    from urllib.error import HTTPError
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen, HTTPError
    from urlparse import urlparse
import json
import sys
import time
import argparse

domain = ''
engine = ''
key = ''
max_queries = 10
sleep = 0
dynamic_filetypes = "asp,aspx,cfm,cgi,jsp,php,phtm,phtml,shtm,shtml"

def main():
    parser = argparse.ArgumentParser(description='Find dynamic pages via Google dorks.')
    parser.add_argument('-d', '--domain', default=domain,
                   help='Specific domain to search (instead of all domains defined in CSE)')
    parser.add_argument('-e', '--engine', default=engine,
                   help='Google custom search engine id (cx value)')
    parser.add_argument('-f', '--filetypes', nargs='?', default=[],
                   const=dynamic_filetypes,
                   help='File extensions to return (if present but no extensions specified, builtin dynamic list is used)')
    parser.add_argument('-k', '--key', default=key,
                   help='Google API key')
    parser.add_argument('-m', '--max-queries', type=int, default=max_queries,
                   help='Maximum number of queries to issue')
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
    data['siteSearch'] = args.domain
    data['q'] = ' '.join(args.terms)
    if args.filetypes:
        filetypes = args.filetypes.split(',')
        data['q'] += ' filetype:' + ' OR filetype:'.join(filetypes)
    data['num'] = 10
    data['start'] = 1

    pages = set()
    found = 0
    query_max_reached = False
    query_count = 0
    data_saved = data['q']

    while query_count < args.max_queries:
        url = 'https://www.googleapis.com/customsearch/v1?'+ urlencode(data)
        try:
            response_str = urlopen(url)
            query_count += 1
            response_str = response_str.read().decode('utf-8')
            response = json.loads(response_str)
        except HTTPError as e:
            response_str = e.read().decode('utf-8')
            response = json.loads(response_str)
            if "Invalid Value" in response['error']['message']:
                sys.exit(0)
            elif response['error']['code'] == 500:
                data['q'] = data_saved
                query_max_reached = True
                continue
            print("error: " + str(response['error']['code']) + " - " + str(response['error']['message']), file=sys.stderr)
            for error in response['error']['errors']:
                print(error['domain'] + "::" + error['reason'] + "::" + error['message'], file=sys.stderr)
            if "User Rate Limit Exceeded" in response['error']['message']:
                print("sleeping " + str(args.sleep) + " seconds", file=sys.stderr)
                time.sleep(5)
            elif args.sleep and "Daily Limit Exceeded" in response['error']['message']:
                print("sleeping " + str(args.sleep) + " seconds", file=sys.stderr)
                time.sleep(args.sleep)
                continue
            else:
                sys.exit(1)
        data_saved = data['q']
        for request in response['queries']['request']:
            if int(request['totalResults']) == 0:
                sys.exit(0)
        for item in response['items']:
            item_url = urlparse(item['link'])
            if item_url.path in pages:
                if not query_max_reached:
                    data['q'] += " -inurl:" + item_url.path
            else:
                pages.add(item_url.path)
                found += 1
                print(item['link'])
        if found >= data['num'] or query_max_reached:
            data['start'] += data['num']

if __name__ == "__main__":
    main()

