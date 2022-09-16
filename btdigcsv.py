import requests
import csv
from bs4 import BeautifulSoup
import re
from os import remove, listdir

keyword = 'trackerName'
filter_csv = list(filter(lambda x: 'torrents.csv' in x, listdir()))

if len(filter_csv) == 1:
    remove("torrents.csv")

def pages_generated(npage):
    return 'https://btdigggink2pdqzqrik3blmqemsbntpzwxottujilcdjfz56jumzfsyd.onion.pet/search?q=' + keyword + '&p=' + npage + '&order=2'

def requests_generated(npage):
    return requests.get(pages_generated(npage))

def soup (npage):
    return BeautifulSoup(requests_generated(npage).text, 'html.parser')

def href_items(npage):
    return soup(npage).find_all('a', attrs={'href': re.compile("^magnet:")})

def div_items(npage):
    return soup(npage).find_all('div', {'class': 'one_result'})

def todo(npage):
    npage = str(npage)
    try:
        torrent_age = str(soup(npage).find(class_='torrent_age').text)
    except AttributeError:
        print('No results found, try another keyword (line 7)')
        exit()

    if torrent_age == 'found 1 day ago':
        print('All pages have been added')
        exit()
    else:
        divs = map(lambda x: x.find(class_='torrent_name').text, div_items(npage))
        sizes = map(lambda x: x.find(class_='torrent_size').text, div_items(npage))
        hrefs = map(lambda x: x.get('href'), href_items(npage))
        
        with open('torrents.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL,delimiter=',')
            writer.writerows(list(zip(divs, sizes, hrefs)))
        print('Adding page ' + npage + ' to your csv')
        npage = int(npage)
        npage += 1
        todo(npage)

todo(0)
