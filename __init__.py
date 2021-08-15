# -*- coding: utf-8 -*-

"""Search onVista stocks.

Synopsis: <trigger> <filter>"""

from albert import *
from locale import getdefaultlocale
from urllib import request, parse
import json
import time
import os

__title__ = "OnVista"
__version__ = "1.0.0"
__triggers__ = "stock "
__authors__ = "Denis Gerber"

iconPath = iconLookup('stock') or os.path.dirname(__file__) + "/stock.png"
baseurl = 'https://www.onvista.de/onvista/boxes/assetSearch.json'
user_agent = "org.albert.extension.python.onvista"
limit = 10

def handleQuery(query):
    if query.isTriggered:
        query.disableSort()

        # avoid rate limiting
        time.sleep(0.1)
        if not query.isValid:
            return

        stripped = query.string.strip()

        if stripped:
            results = []

            params = {
                'searchValue': stripped
            }

            get_url = "%s?%s" % (baseurl, parse.urlencode(params))
            req = request.Request(get_url)

            with request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                stocks = data['onvista']['results']['asset']
                print(stocks[0])

                for i in range(0, min(limit, len(stocks))):
                    stock = stocks[i]
                    title = "%s - %s - %s" % (stock['name'], stock['type'], stock['isin'])
                    summary = ""
                    url = stock['snapshotlink']

                    results.append(Item(id=__title__,
                                        icon=iconPath,
                                        text=title,
                                        subtext=summary if summary else url,
                                        completion=title,
                                        actions=[
                                            UrlAction("Open stock info on OnVista", url),
                                            ClipAction("Copy URL", url)
                                        ]))

            return results
        else:
            return Item(id=__title__,
                        icon=iconPath,
                        text=__title__,
                        subtext="Enter a query to search on onVista")
