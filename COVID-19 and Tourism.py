import csv
from collections import defaultdict
import awoc
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import plotly.express as px

import tkinter as tk
from tkinter import *
from tkinter import ttk


#Setting up csv as dictionary
c = defaultdict(int)

#Reading csv
f = open('coronavirus-disease-covid-19-statistics-and-research.csv','r')
reader = csv.reader(f)

by_country = {}

for row in reader:
    if row[4]=='2020-07-29': #Remove unnecessary dates

        by_country[row[3]] = {'ISO':row[1], 'Continent':row[2], 'Total_cases':float(row[5]),
                              'Population':row[21], 'Population_density':row[22],
                              'Median_age':row[23], 'GDP_per_capita':row[26],
                              'Hospital beds per thousand':row[33]}

        # Removing World values: avoid over counting
        by_country.pop('World',None)

#Making the popup frame and window
window = tk.Tk()
window.title('CFG2020: COVID-19')
window.geometry('800x600')

#Separating window into 2 different frames

top_frame=tk.Frame(window).pack(side='top')
bottom_frame=tk.Frame(window).pack(side='bottom')



#Title label telling us what date the data is taken from
data_label = tk.Label(top_frame,text="Data taken from 'UNCOVER COVID-19 Challenge: \n "
                          "United Network for COVID Data Exploration and Research'",font=("Arial",20)).pack()


#Producing graphs: functions

df = pd.read_csv('coronavirus-disease-covid-19-statistics-and-research.csv')
date = '2020-07-29'

only_july29_df = df.loc[(df['date']== date) & (df['location'] != 'World') & (df['location'] != 'International')]

def gdp_graph():

    gdp_plot = sns.lmplot(x='gdp_per_capita', y='total_cases', data=only_july29_df, hue='continent',legend=False, ci=None)

    plt.xlim(0, None)
    plt.ylim(0, 500000)
    plt.xlabel("GDP per capita /$")
    plt.ylabel('Total cases')
    plt.title("Link between GDP per capita to total cases by country")
    plt.legend(loc='upper right')

    plt.show()

def hospital_beds_graph():

    hospital_beds_plot = sns.lmplot(x='gdp_per_capita',
                                    y='hospital_beds_per_thousand', data=only_july29_df, hue='continent',legend=False,
                                    ci=None) #Removes 95% confidence shading

    plt.xlim(0, None)
    plt.ylim(0, 10)
    plt.xlabel("GDP per capita /$")
    plt.ylabel('Hospital beds per 1000')
    plt.title("Link between GDP per capita to hospital beds")
    plt.legend(loc='upper right')

    plt.show()

#Interactive Map using Plotly
def global_map():
    df_map = pd.read_csv('coronavirus-disease-covid-19-statistics-and-research.csv',usecols=[1,3,4,5], nrows = 33142)

    df_map = df_map.dropna()

    df_countries = df_map.groupby(['date','location']).sum().reset_index()

        #Creating visualization
    fig = px.choropleth(df_countries, locations='location', locationmode = "country names",
                        color="total_cases", hover_name="location", animation_frame='date')

    fig.update_layout( title_text = 'Total Cases Globally', geo=dict(
        showframe=False,
        showcoastlines=False,))

    fig.show()


#Graphical representations
gdp_button = Button(top_frame, text="GDP per capita vs \ntotal cases", command = gdp_graph)
gdp_button.place(x=620, y=100)
hospital_beds_button = Button(top_frame, text="Hospital beds vs \nGDP per capita", command=hospital_beds_graph)
hospital_beds_button.place(x=620, y=150)
global_map_button = Button(top_frame, text="Total cases with \ntimescale map", command=global_map)
global_map_button.place(x=620, y=200)

#Drop down boxes
option_label = tk.Label(top_frame, text="What would you like to know?", font=("Arial",18)).pack()
n = tk.StringVar()
option = ttk.Combobox(window, width = 30, textvariable=n, font=("Arial",15))
option['values']=('Please pick an option','Total cases','Country with the most cases','Country with the least cases')
option.current(0)
option.pack()

region_label = tk.Label(top_frame, text="For which region?", font=("Arial",18)).pack()
m = tk.StringVar()
region = ttk.Combobox(window, width = 30, textvariable=m, font=("Arial",15))
region['values']=('Please pick an option','Africa',
                  'Asia',
                  'Europe',
                  'North America',
                  'Oceania',
                  'South America',
                  'World')
region.current(0)
region.pack()
disclaimer_label = tk.Label(top_frame, text="Based on data from 29/07/2020", font=("Arial",10)).pack()

#Making functions for options
def continent_check(continent_choice):
    all_continents = awoc.AWOC().get_continents_list()
    if continent_choice in all_continents:
        return continent_choice
    else:
        return 'global'

def global_cases():
    global_total_cases = sum(d['Total_cases'] for d in by_country.values() if d)
    result = 'The total number of global cases is {}.'.format(global_total_cases)
    return result

def global_maximum():
    minimum_country_cases = max(d['Total_cases'] for d in by_country.values() if d)

    for country, country_info in by_country.items():
        for key, value in country_info.items():
            if value == minimum_country_cases:
                result = 'The highest number of cases globally is {} ({}).'.format(value, country)
                return result


def global_minimum():
    minimum_country_cases = min(d['Total_cases'] for d in by_country.values() if d)

    for country, country_info in by_country.items():
        for key, value in country_info.items():
            if value == minimum_country_cases:
                result = 'The fewest number of cases globally is {} ({}).'.format(value, country)
                return result

def total_cases(continent_choice):
    choice_total_cases = sum(d['Total_cases'] for d in by_country.values() if d['Continent']==continent_choice)
    result = 'The total number of cases in {} is {}.'.format(continent_choice, choice_total_cases)
    return result

def maximum(continent_choice):
        maximum_country_cases = max(d['Total_cases'] for d in by_country.values() if d['Continent']==continent_choice)

        for country, country_info in by_country.items():
            for key, value in country_info.items():
                if value == maximum_country_cases:
                    result = 'The greatest number of cases in {} is {} ({}).'.format(continent_choice, value, country)
                    return result

def minimum(continent_choice):

        minimum_country_cases = min(d['Total_cases'] for d in by_country.values() if d['Continent']==continent_choice)

        for country, country_info in by_country.items():
            for key, value in country_info.items():
                if value == minimum_country_cases:
                    result = 'The fewest number of cases in {} is {} ({}).'.format(continent_choice, value, country)
                    return result

def error(continent_choice):
    result = "Please pick your options."
    return result

def run_function():
    chosen_option = option.get()
    chosen_region = region.get()
    if continent_check(chosen_region)==chosen_region:
        if chosen_option=='Total cases':
            run_result = total_cases(chosen_region)
        elif chosen_option=='Country with the most cases':
            run_result = maximum(chosen_region)
        elif chosen_option=='Country with the least cases':
            run_result = minimum(chosen_region)

    elif continent_check(chosen_region)=='global':
        if chosen_option=='Total cases':
            run_result = global_cases()
        elif chosen_option=='Country with the most cases':
            run_result = global_maximum()
        elif chosen_option=='Country with the least cases':
            run_result = global_minimum()

    elif continent_check(chosen_region) == 'Please pick an option':
        run_result = error(chosen_region)

    result_label = tk.Label(bottom_frame, text=run_result,font=("Arial", 10)).pack()

run_button = Button(top_frame, text="Go", command=run_function, font=(15)).pack()

window.mainloop()


