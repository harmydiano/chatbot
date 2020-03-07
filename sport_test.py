from bs4 import BeautifulSoup as bs
import requests
import re

url = 'http://sofifa.com/players?offset=0'


fifa_stats = ['Crossing', 'Finishing', 'Heading Accuracy',
              'Short Passing', 'Volleys', 'Dribbling', 'Curve',
              'Free Kick Accuracy', 'Long Passing', 'Ball Control',
              'Acceleration', 'Sprint Speed', 'Agility', 'Reactions',
              'Balance', 'Shot Power', 'Jumping', 'Stamina', 'Strength',
              'Long Shots', 'Aggression', 'Interceptions', 'Positioning',
              'Vision', 'Penalties', 'Composure', 'Marking', 'Standing Tackle',
              'Sliding Tackle', 'GK Diving', 'GK Handling', 'GK Kicking',
              'GK Positioning', 'GK Reflexes']


def soup_maker(url):
    r = requests.get(url)
    markup = r.content
    soup = bs(markup, 'lxml')
    return soup


def find_top_players(soup):
    final_details = {}
    table = soup.find('table', {'class': 'table table-hover persist-area'})
    tbody = table.find('tbody')
    all_a = tbody.find_all('a', {'class': ''})
    all_b = tbody.find_all(href=re.compile("player/"))
    for player in all_a:
        final_details['short_name'] = player.text
        print (final_details)
    for playerb in all_b:
        final_details['links'] = playerb['href']
        #final_details.update(player_all_details('http://sofifa.com' + playerb['href'])
        print ((final_details))




soup = soup_maker(url)
print (find_top_players(soup))