from time import sleep
import csv
import re
from functools import lru_cache
from io import StringIO
from os import rename, remove
from time import sleep

import twill.commands as tc
from bs4 import BeautifulSoup

keyword = 'trackerName'

def rename_oldcsv():
    try:
        rename("torrents.csv", ".torrents.old")
        print('Saving previous search')
    except FileNotFoundError:
        print('Starting search')


def saving_oldcsv():
    try:
        remove('.torrents.old')
    except FileNotFoundError:
        rename_oldcsv()


@lru_cache
def requests_generated(npage):
    print('Generating requests')
    html = StringIO()
    tc.set_output(html)
    sleep(5)
    tc.go('https://btdig.com/search?q=' + keyword + '&p=' + npage + '&order=2')
    tc.show()
    tc.set_output()
    return html.getvalue()


@lru_cache(maxsize=128)
def soup(npage):
    return BeautifulSoup(requests_generated(npage), 'html.parser')


def href_items(npage):
    return soup(npage).find_all('a', attrs={'href': re.compile("^magnet:")})


def div_items(npage):
    return soup(npage).find_all('div', {'class': 'one_result'})


def list_created(npage):
    title = map(lambda x: x.find(class_='torrent_name').text, div_items(npage))
    size = map(lambda x: x.find(class_='torrent_size').text, div_items(npage))
    magnet = map(lambda x: x.get('href'), href_items(npage))
    return list(zip(title, size, magnet))


def rename_csv(npage):
    try:
        rename(".torrents.old", "torrents.csv")
        print('No results found, recovery old csv')
    except:
        if int(npage) == 0:
            print('No results found, try another keyword (line 12)')
        else:
            print('Finished process')


def torrent_age(npage):
    try:
        return str(soup(npage).find(class_='torrent_age').text)
    except AttributeError:
        print('error gordo')
        rename_csv(npage)
        exit()


def listo_csv(npage):
    npage = str(npage)
    if torrent_age(npage) == 'found 1 day ago':
        print('All pages have been added')
        exit()
    with open('torrents.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=',')
        writer.writerows(list_created(npage))
    print('Adding page ' + npage + ' to your csv')

    npage = int(npage)
    npage += 1
    listo_csv(npage)


saving_oldcsv()

listo_csv(0)
