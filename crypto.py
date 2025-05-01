from bs4 import BeautifulSoup
import re
import requests
import json

html_content = requests.get("https://coinmarketcap.com/").text

soup = BeautifulSoup(html_content, "html.parser")

rows = soup.find_all("tr",style=re.compile("cursor")) 
results = {}
i=1
for row in rows:
    try:
        rank_tag = row.find("p", class_=re.compile(r"sc-71024e3e-0"))
        rank = rank_tag.text.strip() if rank_tag else None

        name_tag = row.find("span", class_=re.compile(r"coin-item-name"))
        symbol_tag = row.find("p", class_=re.compile(r"coin-item-symbol"))
        name = name_tag.text.strip() if name_tag else None
        symbol = symbol_tag.text.strip() if symbol_tag else None

        price_tag = row.find("div", class_="sc-142c02c-0")
        price = price_tag.find("span").text.strip() if price_tag else None

        market_cap_tag = row.find("span", class_=re.compile(r"sc-11478e5d-0"))
        market_cap = market_cap_tag.text.strip() if market_cap_tag else None

        change_rate = row.find("a", href=re.compile(r"#markets"))
        change = change_rate.find("p").text.strip() if volume_tag else None


        results[rank]={
                "currency": symbol,
                "price": price,
                "market capital": market_cap,
                "daily change rate": change}
    except Exception as e:
        print(f"Error parsing row: {e}")

with open("crypto.json","w") as file:
    json.dump(results,file,indent=4)
