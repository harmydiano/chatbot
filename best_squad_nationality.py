# Import libraries
from __future__ import print_function
import sys
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt #%matplotlib inline

from plotly.offline import iplot, init_notebook_mode
from geopy.geocoders import Nominatim
import plotly.plotly as py

FIFA18 = pd.read_csv('CompleteDataset.csv', low_memory=False)
FIFA18.columns

interesting_columns = [
    'Name',
    'Age',
    'Nationality',
    'Overall',
    'Potential',
    'Club',
    'Value',
    'Wage',
    'Preferred Positions'
]
FIFA18 = pd.DataFrame(FIFA18, columns=interesting_columns)

def str2number(amount):
    if amount[-1] == 'M':
        return float(amount[1:-1]) * 1000000
    elif amount[-1] == 'K':
        return float(amount[1:-1]) * 1000
    else:
        return float(amount[1:])


FIFA18['ValueNum'] = FIFA18['Value'].apply(lambda x: str2number(x))
FIFA18['WageNum'] = FIFA18['Wage'].apply(lambda x: str2number(x))
FIFA18['Position'] = FIFA18['Preferred Positions'].str.split().str[0]

# Grouping the data by countries
valcon = FIFA18.groupby("Nationality").size().reset_index(name="Count")

#best squad analysis
FIFA18 = FIFA18[['Name', 'Age', 'Nationality', 'Overall', 'Potential', 'Club', 'Position', 'Value', 'Wage']]
#print (FIFA18.head(10))


def get_best_squad(formation):
    FIFA18_copy = FIFA18.copy()
    store = []

    # iterate through all positions in the input formation and get players with highest overall respective to the position
    for i in formation:
        store.append([
            i,
            FIFA18_copy.loc[[FIFA18_copy[FIFA18_copy['Position'] == i]['Overall'].idxmax()]]['Name'].to_string(
                index=False),
            FIFA18_copy[FIFA18_copy['Position'] == i]['Overall'].max(),
            FIFA18_copy.loc[[FIFA18_copy[FIFA18_copy['Position'] == i]['Overall'].idxmax()]]['Age'].to_string(
                index=False),
            FIFA18_copy.loc[[FIFA18_copy[FIFA18_copy['Position'] == i]['Overall'].idxmax()]]['Club'].to_string(
                index=False),
            FIFA18_copy.loc[[FIFA18_copy[FIFA18_copy['Position'] == i]['Overall'].idxmax()]]['Value'].to_string(
                index=False),
            FIFA18_copy.loc[[FIFA18_copy[FIFA18_copy['Position'] == i]['Overall'].idxmax()]]['Wage'].to_string(
                index=False)
        ])

        FIFA18_copy.drop(FIFA18_copy[FIFA18_copy['Position'] == i]['Overall'].idxmax(),
                         inplace=True)

    # return store with only necessary columns
    return pd.DataFrame(np.array(store).reshape(11, 7),
                        columns=['Position', 'Player', 'Overall', 'Age', 'Club', 'Value', 'Wage']).to_string(
        index=False)


def get_best_squad_n(formation, nationality, measurement='Overall'):
    FIFA18_copy = FIFA18.copy()
    FIFA18_copy = FIFA18_copy[FIFA18_copy['Nationality'] == nationality]
    store = []

    for i in formation:
        store.append([
            FIFA18_copy.loc[[FIFA18_copy[FIFA18_copy['Position'].str.contains(i)][measurement].idxmax()]][
                'Position'].to_string(index=False),
            FIFA18_copy.loc[[FIFA18_copy[FIFA18_copy['Position'].str.contains(i)][measurement].idxmax()]][
                'Name'].to_string(index=False),
            FIFA18_copy[FIFA18_copy['Position'].str.contains(i)][measurement].max(),
            FIFA18_copy.loc[[FIFA18_copy[FIFA18_copy['Position'].str.contains(i)][measurement].idxmax()]][
                'Age'].to_string(index=False),
            FIFA18_copy.loc[[FIFA18_copy[FIFA18_copy['Position'].str.contains(i)][measurement].idxmax()]][
                'Club'].to_string(index=False),
            FIFA18_copy.loc[[FIFA18_copy[FIFA18_copy['Position'].str.contains(i)][measurement].idxmax()]][
                'Value'].to_string(index=False),
            FIFA18_copy.loc[[FIFA18_copy[FIFA18_copy['Position'].str.contains(i)][measurement].idxmax()]][
                'Wage'].to_string(index=False)
        ])

        FIFA18_copy.drop(FIFA18_copy[FIFA18_copy['Position'].str.contains(i)][measurement].idxmax(),
                         inplace=True)

    return np.mean([x[2] for x in store]).round(2), pd.DataFrame(np.array(store).reshape(11, 7),
                                                                 columns=['Position', 'Player', measurement, 'Age',
                                                                          'Club', 'Value', 'Wage']).to_string(
        index=False)


def get_summary_n(squad_list, squad_name, nationality_list):
    summary = []

    for i in nationality_list:
        count = 0
        for j in squad_list:
            # for overall rating
            O_temp_rating, _ = get_best_squad_n(formation=j, nationality=i, measurement='Overall')

            # for potential rating & corresponding value
            P_temp_rating, _ = get_best_squad_n(formation=j, nationality=i, measurement='Potential')

            summary.append([i, squad_name[count], O_temp_rating.round(2), P_temp_rating.round(2)])
            count += 1

    return summary

squad_343_strict = ['GK', 'CB', 'CB', 'CB', 'RB|RWB', 'CM|CDM', 'CM|CDM', 'LB|LWB', 'RM|RW', 'ST|CF', 'LM|LW']
squad_442_strict = ['GK', 'RB|RWB', 'CB', 'CB', 'LB|LWB', 'RM', 'CM|CDM', 'CM|CAM', 'LM', 'ST|CF', 'ST|CF']
squad_4312_strict = ['GK', 'RB|RWB', 'CB', 'CB', 'LB|LWB', 'CM|CDM', 'CM|CAM|CDM', 'CM|CAM|CDM', 'CAM|CF', 'ST|CF', 'ST|CF']
squad_433_strict = ['GK', 'RB|RWB', 'CB', 'CB', 'LB|LWB', 'CM|CDM', 'CM|CAM|CDM', 'CM|CAM|CDM', 'RM|RW', 'ST|CF', 'LM|LW']
squad_4231_strict = ['GK', 'RB|RWB', 'CB', 'CB', 'LB|LWB', 'CM|CDM', 'CM|CDM', 'RM|RW', 'CAM', 'LM|LW', 'ST|CF']

squad_list = [squad_343_strict, squad_442_strict, squad_4312_strict, squad_433_strict, squad_4231_strict]
squad_name = ['3-4-3', '4-4-2', '4-3-1-2', '4-3-3', '4-2-3-1']

def team(national_team,team_formation):
    national_team = national_team.lower().title()
    France = pd.DataFrame(np.array(get_summary_n(squad_list, squad_name, [national_team])).reshape(-1,4), columns = ['Nationality', 'Squad', 'Overall', 'Potential'])
    France.set_index('Nationality', inplace = True)
    France[['Overall', 'Potential']] = France[['Overall', 'Potential']].astype(float)

    #print (France)
    if team_formation ==443:

        rating_433_FR_Overall, best_list_433_FR_Overall = get_best_squad_n(squad_433_strict, national_team, 'Overall')
        print('-Overall-')
        print('Average rating: {:.1f}'.format(rating_433_FR_Overall))
        print(best_list_433_FR_Overall)
    elif team_formation == 442:
        rating_442_FR_Potential, best_list_442_FR_Potential = get_best_squad_n(squad_442_strict, national_team, 'Potential')
        print('-Potential-')
        print('Average rating: {:.1f}'.format(rating_442_FR_Potential))
        print(best_list_442_FR_Potential)
    elif team_formation ==343:
        rating_343_ARG_Overall, best_list_343_ARG_Overall = get_best_squad_n(squad_343_strict, national_team, 'Overall')
        print('-Overall-')
        print('Average rating: {:.1f}'.format(rating_343_ARG_Overall))
        print(best_list_343_ARG_Overall)
    else:
        rating_4231_GER_Potential, best_list_4231_GER_Potential = get_best_squad_n(squad_4231_strict, national_team,
                                                                                   'Potential')
        print('-Potential-')
        print('Average rating: {:.1f}'.format(rating_4231_GER_Potential))
        print(best_list_4231_GER_Potential)

team('nigeria',442)

