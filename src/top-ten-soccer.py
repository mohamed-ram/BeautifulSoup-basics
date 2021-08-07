from src.utils import append_to_column, clear_data

from bs4 import BeautifulSoup
import pandas as pd
import requests

base_url = "https://en.wikipedia.org/wiki/World_Soccer_(magazine)"

# get request..
page = requests.get(base_url)

# type of page is "Response".
print(type(page))

# request status code
print(page.status_code)

# 200 == requests.status_codes.codes.ok
if page.status_code == 200:
    bs = BeautifulSoup(page.text, "lxml")

    all_players = bs.find("div", class_="mw-parser-output").find_all("ul")[9].find_all("li")
    top_ten = all_players[-10:]
    
    data = {
        "Year": [],
        "Country": [],
        "Player": [],
        "Team": []
    }
    
    # print(top_ten)
    # player = top_ten[5]
    for player in top_ten:
        # get year and add it to data["Year"]
        year = player.find("span").previousSibling.split()[0]
        if year:
            data["Year"].append(year)
        else:
            data["Year"].append("None")
        
        # get country name and add it to data["Country"]
        country = player.find("img")["src"].split("Flag_of_")[1].split(".")[0]
        if country:
            data["Country"].append(country)
        else:
            data["Country"].append("None")

        # get player name and add it to data["Player"]
        player_name = player.find("a")["title"]
        if player_name:
            data["Player"].append(player_name)
        else:
            data["Player"].append("None")

        # get team name and add it to data["Team"]
        team = player.find_all("a")[1]["title"]
        if team:
            data["Team"].append(team)
        else:
            data["Team"].append("None")


    # clear_data(data)
    
    # use pandas.
    table = pd.DataFrame(data)
    table.index = table.index + 1
    
    # export to csv file.
    table.to_csv("data/top-ten-soccer.csv", sep=",", index=False, encoding="utf-8")
    print(table)
        



