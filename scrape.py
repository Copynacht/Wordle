from urllib import request
from bs4 import BeautifulSoup
import ssl, re
ssl._create_default_https_context = ssl._create_unverified_context

hList = []
wList = []
next_href = ''

for x in range(97, 123):
    next_href=0
    while True:
        url = 'https://cotobasearch.com/search/results?req=7&pos=5&cat=all'
        url = url + '&let=' +chr(x)
        if next_href != 0:
            url = next_href
        print(url)
        response = request.urlopen(url)
        bs = BeautifulSoup(response, 'html.parser')
        next = bs.find('link', rel= 'next') 
        if next != None:
            next_href = next.get('href')
        else:
            break
        hList = bs.find_all('font', style='font-weight:bold;')
        for h in hList:
            wList.append(h.text)
        response.close()

for x in range(97, 123):
    url = 'https://kanji.reader.bz/english/starting/'
    url = url + chr(x) + '/5'
    print(url)
    response = request.urlopen(url)
    bs = BeautifulSoup(response, 'html.parser')
    hList = re.finditer('(?<=">)[a-zA-Z]{5}(?=\s)', str(bs))
    for h in hList: 
        wList.append(h.group())
    response.close()


for x in range(97, 123):
    url = 'https://www.kashiramoji.com/kashira-'
    url = url + chr(x) + '/'
    print(url)
    response = request.urlopen(url)
    bs = BeautifulSoup(response, 'html.parser')
    hList = re.finditer('(?<=")[a-zA-Z]{5}(?=|)', str(bs))
    for h in hList: 
        wList.append(h.group())
    response.close()

wList = list(set(wList))

with open('wlist.txt', 'w') as f:
    for d in wList:
        f.write("%s\n" % d)