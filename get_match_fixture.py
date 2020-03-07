from bs4 import BeautifulSoup as bs
import requests
import re
from datetime import date

#fetch the group stage from bbc url
url='https://www.bbc.com/sport/football/world-cup/schedule/group-stage'
#get current date and append to the fixtures url to iterate on each match
today = str(date.today())
fixture_url = 'http://kwese.espn.com/football/fixtures/_/date/20180616/league/fifa.world'

def soup_maker(fixture_url):
    r = requests.get(fixture_url)
    markup = r.content
    soup = bs(markup, 'lxml')
    return soup

def group_stage(soup):
    final_details = {}
    table = soup.find('div', {'class': 'responsive-table-wrap'})
    all_a = table.find('table', {'class': 'schedule has-team-logos soccer align-left'})
    all_a = all_a.find('tbody')
    all_a = all_a.find_all('abbr')
    list =[]
    for a in (all_a):
        a = a.prettify()
        list.append(a)
    return (list)
    #all_a = all_a.replace('v', ' VS ')

    #group_fixture = group_fixture.text.replace(',','\n')
    #return ("GROUP STAGE \n %s \n MATCH FIXTURE \n %s") %(all_a,group_fixture)

soup = soup_maker(fixture_url)
#print (group_stage(soup))
b= (group_stage(soup))
b_length = len(b)
print (b)


#print (match_scores(soup))