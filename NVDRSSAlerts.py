#!/usr/bin/python

from bs4 import BeautifulSoup
import requests

feeds = {}
keywords = []

with open ('feedList', 'r') as f:
    for line in f.readlines():
        lineSplit = line.split(',')
        feeds[lineSplit[0]] = lineSplit[1]

with open('keywords', 'r') as f:
    keywords = [line.strip() for line in f.readlines()]


def parseFeed(RSSFeed):
    parsedFeed = []
    RSSResponse = requests.get(RSSFeed.strip())  
    soup = BeautifulSoup(RSSResponse.content, 'html.parser')
    items = soup.find_all('item')

    for item in items:
        parsedFeed.append({"title":item.title, "link":item.link, "desc":item.description}) # needs to be tailored to the feed

    return parsedFeed


def findMatches(RSSData, keywords):
    for item in RSSData:
        for exp in keywords:
            if exp in item['desc']:
                print(' > MATCH on %s: Look at %s\n%s' % exp, item['title'], item['link'])


for feed, rss in feeds.items():
    print("Checking [%s] for updates..." % feed)
    findMatches(parseFeed(rss), keywords)
