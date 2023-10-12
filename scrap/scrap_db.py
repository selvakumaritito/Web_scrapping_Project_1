from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import sqlite3
try:
    response=requests.get("https://www.imdb.com/search/title/?companies=co0144901")
    soup = BeautifulSoup(response.text, 'html.parser')
    movies=soup.find("div", class_="lister-list").find_all("div",class_="lister-item")
    movies_list = {"Movie_Index": [], "Movie_Name": [], "Year": [], "Genre": [],"Rate": [], "Story": [], "Vote": []}
    
    for movie in movies:
        #print(movie)
        index = movie.find("h3").find('span',class_='lister-item-index').get_text(strip=True).split('.')[0]
        name=movie.find("h3").a.get_text(strip=True)
        year = movie.find("h3").find('span',class_='lister-item-year').get_text(strip=True).replace('(',"")
        #year=re.sub('\D',"", year)
        year=year.replace(')',"")
        Genre=movie.find("p", class_='text-muted').find('span',class_='genre').get_text(strip=True)
        rate=movie.find("div",class_="ratings-imdb-rating").strong.text
        story=movie.find("p").findNext("p").get_text(strip=True)
        #stars=movie.find("p").findNext("p").findNext("p").find('span',class_='ghost').get_text()
        #votes=movie.find('p').findNext("p").findNext("p").findNext("p").find('span').findNext('span').get_text(strip=True)
        votes=movie.find('p').findNext("p").findNext("p").findNext("p").find_all('span')[-1].get_text(strip=True)

        #print(index, name, year,Genre,rate, story,votes)
        movies_list["Movie_Index"].append(index)
        movies_list["Movie_Name"].append(name)
        movies_list["Year"].append(year)
        movies_list["Genre"].append(Genre)
        movies_list["Rate"].append(rate)
        movies_list["Story"].append(story)
        movies_list["Vote"].append(votes)

        
except Exception as e:
    print (e)

df=pd.DataFrame(data=movies_list)
print(df.head)
data_to_insert = [tuple(row) for row in df.values]
connection=sqlite3.connect("scrap.db")
cursor=connection.cursor()
query="create table if not exists movie_list(Movie_Index, Movie_Name, Year, Genre, Rate, Story, Vote)"
cursor.execute(query)

query1 = "INSERT INTO movie_list VALUES (?, ?, ?, ?, ?, ?, ?)"
cursor.executemany(query1, data_to_insert)

connection.commit()
connection.close()