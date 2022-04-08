from os import sep
import requests
from bs4 import BeautifulSoup

url = "https://www.ceneo.pl/101052360#tab=reviews"
response = requests.get(url)

page = BeautifulSoup(response.text, "html.parser")

opinions = page.select("div.js_product-review")
opinion = opinions.pop(0)
opinion_id = opinion["data-entry-id"]
author = opinion.select_one("span.user-post__author-name").get_text().strip()
recommendation = opinion.select_one("span.user-post__author-recomendation > em").get_text().strip()
stars = opinion.select_one("span.user-post__score-count").get_text().strip()
content = opinion.select_one("div.user-post__text").get_text().strip()
pros = [positives.get_text().strip() for positives in opinion.select("div[class$=positives] ~ div.review-feature__item")]
cons = [negatives.get_text().strip() for negatives in opinion.select("div[class$=negatives] ~ div.review-feature__item")]
useful = opinion.select_one("button.vote-yes > span").get_text().strip()
useless = opinion.select_one("button.vote-no > span").get_text().strip()
published = opinion.select_one("span.user-post__published > time:nth-child(1)")["datetime"]
purchased = opinion.select_one("span.user-post__published > time:nth-child(2)")["datetime"]

print(author, recommendation, stars, content, pros, cons, useful, useless, published, purchased, sep="\n")