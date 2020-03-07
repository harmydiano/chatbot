from bs4 import BeautifulSoup as bs
import requests
import re
from datetime import date

#fetch the group stage from bbc urlcd
url='https://www.bbc.com/sport/football/world-cup/schedule/group-stage'
#get current date and append to the fixtures url to iterate on each match
today = str(date.today())
fixture_url = 'https://www.bbc.com/sport/football/world-cup/scores-fixtures/%s' %(today)

def soup_maker(url):
    r = requests.get(url)
    markup = r.content
    soup = bs(markup, 'lxml')
    return soup

def group_stage(soup,group_code):
    final_details = {}
    table = soup.find('div', {'class': 'group-stage gel-layout__item','id':'group-stage--%s' % group_code})
    all_a = table.find('table', {'class': 'table group-stage__table'})
    all_a = all_a.text.replace('   ','\n')
    group_fixture = table.find('ul', {'class': 'fixture-list'})
    group_fixture = group_fixture.prettify()
    return ("GROUP STAGE \n %s \n MATCH FIXTURE \n %s") %(all_a,group_fixture)

soup = soup_maker(url)

print (match_scores(soup))

def main():
    assert len(sys.argv) >= 3
    function = sys.argv[1]
    #function = 'realtime'
    term = ''.join(sys.argv[2:])
    #term = 'ondo'
    if function == 'realtime':
        #location = querylocation(term)
        location = True
        if location:
            print(group_stage(soup, term))

if __name__ == '__main__':
    main()