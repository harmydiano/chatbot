from bs4 import BeautifulSoup as bs
import requests
import re
from datetime import date
import string
from random import randint
#fetch the group stage from bbc url
url='https://www.bbc.com/sport/football/world-cup/schedule/group-stage'
#get current date and append to the fixtures url to iterate on each match
today = str(date.today())
fixture_url = 'http://www.newsnow.co.uk/h/Sport/Football/2018+FIFA+World+Cup'

def soup_maker(fixture_url):
    r = requests.get(fixture_url)
    markup = r.content
    soup = bs(markup, 'lxml')
    return soup

def group_stage(soup):
    final_details = {}
    table = soup.find('div', {'class': 'newsbox_inner'})
    with open('w_news.txt', 'a',encoding='utf-8') as file:
        file.write(table.text)

def viewItem():
    remove_empty_lines('w_news.txt')
    f = open('w_news.txt', 'r')
    data = f.readlines()
    return (data)

def remove_empty_lines(filename):
    """Overwrite the file, removing empty lines and lines that contain only whitespace."""
    with open(filename, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.writelines(line for line in lines if line.strip())
        f.truncate()

soup = soup_maker(fixture_url)
#print (group_stage(soup))
group_stage(soup)
a = viewItem()
b=len(a)
random_number = (randint(2, 10))
print (a[-random_number])


