# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

from io import open
from os import environ
from sys import exit

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


DELIMITER = '|'
# CHROME_RESOURCES_ROOT = environ['HOME'] + '/Library/Application Support/Google/Chrome/Default/' ?
HOME_PATH = environ['HOME']
CHROME_RESOURCES_ROOT = HOME_PATH + '/Library/Application Support/Google/Chrome/Profile 1/'


def copy_buf():
    from shutil import copy
    # Chromeがファイルロックをかけている？
    copy(CHROME_RESOURCES_ROOT + '/History', HOME_PATH + '/tmp/History')
    copy(CHROME_RESOURCES_ROOT + '/Bookmarks', HOME_PATH + '/tmp/Bookmarks')


def _get_history():
    import sqlite3
    # con = sqlite3.connect(HOME_PATH + '/Library/Application\ Support/Google/Chrome/Default/History')
    con = sqlite3.connect(HOME_PATH + '/tmp/History')
    cursor = con.execute('SELECT visits.url, urls.title, urls.url FROM visits LEFT JOIN urls ON visits.url = urls.id GROUP BY visits.url ORDER BY urls.visit_count DESC;')
    from urlparse import urlparse
    for row in cursor:
        if row[1]:
            yield row[1] + DELIMITER + row[2]
        else:
            # titleがなければドメイン名（っぽい部分）で代用
            yield urlparse(row[2]).netloc + DELIMITER + row[2]


def _get_bookmarks():
    import json
    with open(HOME_PATH + '/tmp/Bookmarks') as json_f:
        content = json.loads(json_f.read())['roots']
    bookmark_bar = content['bookmark_bar']
    others = content['other']
    from itertools import chain
    return chain(
        _extract(bookmark_bar),
        _extract(others),
    )


def _extract(child):
    if child['type'] == 'url':
        yield child['name'] + DELIMITER + child['url']
    elif child['type'] == 'folder':
        for chi in child['children']:
            # same as `yield from _extract(chi)`
            for c in _extract(chi): yield c
    else:
        raise StopIteration()



def extract_urlhistory_title_and_url():
    from peco import Peco
    brows_hitory = _get_history()
    peco = Peco()
    result, err = peco.filter('\n'.join(brows_hitory))
    if not result:
        exit(1)
    if err:
        print(err)
        exit(1)
    result = result.strip()
    return result.split(DELIMITER)


def extract_bookmark_title_and_url():
    from peco import Peco
    bookmarks = _get_bookmarks()
    peco = Peco()
    result, err = peco.filter('\n'.join(bookmarks))
    if not result:
        exit(1)
    if err:
        print(err)
        exit(1)
    result = result.strip()
    return result.split(DELIMITER)


if __name__ == '__main__':
    copy_buf()  # TODO: 条件どうしよ
    # title, url = extract_urlhistory_title_and_url()
    title, url = extract_bookmark_title_and_url()
    print(url)
