import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = 'Movies.db'
table_name = 'Top_50'
csv_path = 'top_50_films.csv'
df = pd.DataFrame(columns=["Average Rank", "Film", "Year"])
count = 0

html_page = requests.get(url).text # Page code
data = BeautifulSoup(html_page, 'html.parser')

tables = data.find_all('tbody') # Find all tables in data
rows = tables[0].find_all('tr') # Rows of the first table

for row in rows:
    if count < 50:
        col = row.find_all('td') # For each row, access its elements
        if len(col) != 0: # If row has data
            data_dict = {
                "Average Rank": col[0].contents[0],
                "Film": col[1].contents[0],
                "Year": col[2].contents[0]
            }
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df, df1], ignore_index=True)
            count += 1
    else:
        break

print(df)
df.to_csv(csv_path) #Turns the DF into a csv file


conn = sqlite3.connect(db_name)
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()