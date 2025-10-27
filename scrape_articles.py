import bs4
import requests
import os
import pandas as pd


urls = []

with open("article_urls.txt", 'r', encoding='utf-8') as f:
    for line in f:
        urls.append(line)

for i in range(len(urls)):
    curr_url = urls[i]
    urls[i] = curr_url[0:len(curr_url)-1]

for i in range(20):
    current_url = urls[i]
    raw_article = requests.get(current_url)
    souped_article = bs4.BeautifulSoup(raw_article.text, 'html.parser')
    file_name = 'article-' + str(i) + '.txt'
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(str(souped_article))