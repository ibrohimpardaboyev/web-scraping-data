import requests 
import pandas as pd
from bs4 import BeautifulSoup
page = 1
dic={
    'title': [],
    'rating': [],
    'price': [],
    'instock': []
}
# while True:
#     try:
while True:
    resp = requests.get(f'https://books.toscrape.com/catalogue/page-{page}.html')
    soup = BeautifulSoup(resp.text)
    try:
        soup.find("center").text.strip()!="404 Not Found"
        break
    except:
        str_to_int = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }
        webpage = soup.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        for i in webpage:
            dic['title'].append(i.find("h3").a['title'])
            dic["rating"].append(str_to_int[i.find("p").get('class')[1]])
            dic["price"].append(float(i.find("p","price_color").text[2:]))
            dic["instock"].append(True if soup.find("p",class_ = "instock availability").text.strip() == "In stock" else False) 
        page=page + 1
df=pd.DataFrame(dic)
df.to_csv("movies.csv",index=False)