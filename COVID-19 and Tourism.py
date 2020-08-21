import csv
import pandas as pd

def read_data():

    file = 'datasets_494766_1402868_country_wise_latest.csv'
    with open(file) as confirmed_cases_csv:
        spreadsheet = csv.DictReader(confirmed_cases_csv)
        for row in spreadsheet:
            if row['WHO Region'] == 'Europe':
                print(row)

data = read_data()

df = pd.read_csv('datasets_494766_1402868_country_wise_latest.csv', sep=",", header=None)
print(df)
'''
for row in data:
    print(country['Country/Region'])

for row in data:

    if row['WHO Region'] == 'Europe':

        max_confirmed_case = max(data,items(), key= lambda x : x[1])
        print(max_confirmed_case[1], max_confirmed_case[0])

'''