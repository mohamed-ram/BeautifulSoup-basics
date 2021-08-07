import requests
from bs4 import BeautifulSoup
import pandas as pd


data = {
        "Title": [],
        "Price": [],
        "Date": [],
        "Address": []
    }

# get all listings up to specific page..
pages_to = 5

def get_data():
    page_number = 1
    while page_number <= pages_to:
        base_url = f"https://losangeles.craigslist.org/d/for-sale/search/sss?s={page_number}&query=car&sort=rel"
    
        # get response from base url..
        page = requests.get(base_url)
        if page.status_code == 200:
            
            # initialize beautifulSoup..
            bs = BeautifulSoup(page.text, "lxml")
           
            # get cars list
            cars_list = bs.find("ul", id="search-results").find_all("li", "result-row")
            
            for car in cars_list:
                # car price
                price = car.find("span", class_="result-meta").find("span", class_="result-price")
                if price:
                    if price.text:
                        data["Price"].append(price.text)
                    else:
                        data["Price"].append("None")
                else:
                    data["Price"].append("None")
        
                # car title
                title = car.find("div", class_="result-info").find("a", class_="result-title")
                if title:
                    if title.text:
                        data["Title"].append(title.text)
                    else:
                        data["Title"].append("None")
                else:
                    data["Title"].append("None")
        
                # date of publish
                date = car.find("time")["title"]
                if date:
                    data["Date"].append(date)
                else:
                    data["Date"].append("None")
        
                # address
                address = car.find("span", class_="result-hood")
                if address:
                    if address.text:
                        data["Address"].append(address.text.strip()[1: -1])
                    else:
                        data["Address"].append("None")
                else:
                    data["Address"].append("None")
        
        page_number += 1
        
    table = pd.DataFrame(data)
    table.index = table.index + 1
    
    # export to csv file.
    table.to_csv("data/craigslist-cars-scraping.csv", index=False, encoding="utf-8")
    print(table)



# price = cars_list[1].find("span", class_="result-meta").find("span", class_="result-price")
# print(price)



if __name__ == "__main__":
    get_data()

