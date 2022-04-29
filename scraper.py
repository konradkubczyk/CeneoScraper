import requests
import json
from bs4 import BeautifulSoup

url = "https://www.ceneo.pl/101052360#tab=reviews"
all_opinions = []

while(url):
    response = requests.get(url)

    page = BeautifulSoup(response.text, "html.parser")
    opinions = page.select("div.js_product-review")

    for opinion in opinions:
        opinion_id = opinion["data-entry-id"]
        author = opinion.select_one("span.user-post__author-name").get_text().strip()
        try:
            recommendation = opinion.select_one("span.user-post__author-recomendation > em").get_text().strip()
        except AttributeError:
            recommendation = None
        stars = opinion.select_one("span.user-post__score-count").get_text().strip()
        content = opinion.select_one("div.user-post__text").get_text().strip()
        useful = opinion.select_one("button.vote-yes > span").get_text().strip()
        useless = opinion.select_one("button.vote-no > span").get_text().strip()
        published = opinion.select_one("span.user-post__published > time:nth-child(1)")["datetime"]
        try:
            purchased = opinion.select_one("span.user-post__published > time:nth-child(2)")["datetime"]
        except TypeError:
            purchased = None
        pros = [item.get_text().strip() for item in opinion.select("div[class$=positives] ~ div.review-feature__item")]
        cons = [item.get_text().strip() for item in opinion.select("div[class$=negatives] ~ div.review-feature__item")]

        single_opinion = {
            "opinion_id": opinion_id,
            "author": author,
            "recommendation": recommendation,
            "stars": stars,
            "content": content,
            "pros": pros,
            "cons": cons,
            "useful": useful,
            "useless": useless,
            "published": published,
            "purchased": purchased,
        }
        all_opinions.append(single_opinion)
    
    try:
        url = "https://www.ceneo.pl"+page.select_one("a.pagination__next")["href"]
    except TypeError:
        url = None

with open("opinions/101052360.json", "w", encoding="UTF-8") as jfile:
    json.dump(all_opinions, jfile, indent=4, ensure_ascii=False)
