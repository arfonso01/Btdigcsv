import requests
import json
from time import sleep
import csv
from bs4 import BeautifulSoup
import re
from os import rename, remove
from functools import lru_cache

keyword = 'trackerName'

headers = {
    "Content-Type": "application/json"
}

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
    sleep(6)
    create_url = '"http://btdig.com/search?q=' + keyword + '&p=' + npage + '&order=2"'

    data_raw = {
        '"cmd"': '"request.get"',
        '"url"': create_url,
        '"maxTimeout"': 60000
    }
    data_raw = f"{data_raw}"
    data_raw = data_raw.replace("'","")
    url = 'http://localhost:8191/v1'
    request = json.loads(requests.post(url, headers=headers, data=data_raw).text)
    return request["solution"]["response"]


@lru_cache(maxsize=128)
def soup (npage):
    return BeautifulSoup(requests_generated(npage), 'lxml')

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
            print('No results found, try another keyword (line 7)')
        else:
            print('Finished process')


def torrent_age(npage):
    try:
        return str(soup(npage).find(class_='torrent_age').text)
        # return str(requests_generated(npage).find(class_='torrent_age').text)
    except AttributeError:
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
