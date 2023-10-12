from bs4 import BeautifulSoup
import requests,openpyxl
import re


excel = openpyxl.Workbook()
sheet = excel.active
sheet.title="Movies List"
sheet.append(['Index','Movie Name', 'Year','Genre','Rating','Story','Votes'])

try:
    response=requests.get("https://www.imdb.com/search/title/?companies=co0144901")
    soup = BeautifulSoup(response.text, 'html.parser')
    movies=soup.find("div", class_="article").find_all("div",class_="lister-item")
    

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
        sheet.append([index, name, year,Genre,rate, story,votes])
       

except Exception as e:
    print (e)

excel.save("Movie_list.xlsx")