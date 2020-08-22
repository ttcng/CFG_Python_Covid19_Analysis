import pandas as pd
import awoc

continents_list = awoc.AWOC().get_continents_list()

df = pd.read_csv('coronavirus-disease-covid-19-statistics-and-research.csv')

africa_country = []
africa_value = []

antarctica_country = []
antarctica_value = []

asia_country = []
asia_value = []

europe_country = []
europe_value = []

na_country = []
na_value = []

oceania_country = []
oceania_value = []

sa_country = []
sa_value = []

country_list = [africa_country,antarctica_country,asia_country,europe_country,na_country,oceania_country,sa_country]
value_list = [africa_value,antarctica_value,asia_value,europe_value,na_value,oceania_value,sa_value]

i=0

for index, row in df.iterrows():
    if row['date']=="2020-07-29":
        if row['continent']==continents_list[i]:
            country = row['location']
            country_list[i].append(country)

            value = row['total_cases']
            value_list[i].append(value)

        elif row['continent'] == continents_list[i+2]:
            country = row['location']
            country_list[i+2].append(country)

            value = row['total_cases']
            value_list[i+2].append(value)




print(africa_country)
print(africa_value)
print(asia_country)
print(asia_value)



