import bs4
import requests
import os
import pandas as pd


urls = []
FRAUD_KEYWORDS = ['fraud', 'scam', 'embezzlement', 'whistleblower', 'corruption', 'racketeering', 'transaction failure', 'irregularity', 'exposure', 'non-compliance', 'error']

with open("article_urls.txt", 'r', encoding='utf-8') as f:
    for line in f:
        urls.append(line)

for i in range(len(urls)):
    curr_url = urls[i]
    urls[i] = curr_url[0:len(curr_url)-1]

articles_df = pd.DataFrame(columns=['title','author','text'])

articles_found = 0

for i in range(len(urls)):
    keywords_found = 0
    current_url = urls[i]
    raw_article = requests.get(current_url)
    souped_article = bs4.BeautifulSoup(raw_article.text, 'html.parser')
    file_name = 'article-' + str(i) + '.txt'
    #with open(file_name, 'w', encoding='utf-8') as f:
    #    f.write(str(souped_article))
    article_title = souped_article.find('h1')
    article_author = souped_article.find('h5', class_='margin-top-1')
    article_body = souped_article.find('div', class_="cell large-8")
    for keyword in FRAUD_KEYWORDS:
        if keyword in str(article_body):
            keywords_found += 1
    #article_write = article_title.text + '\n' + article_author.text + '\n' + article_body.text
    #file_name_2 = 'article-text-' + str(i) + '.txt'
    #with open(file_name_2, 'w', encoding='utf-8') as f:
    #    f.write(str(article_write))
    if keywords_found > 0:
        articles_found += 1
        curr_article = pd.DataFrame({'title':[article_title], 'author':[article_author], 'text':[article_body]})
        articles_df = pd.concat([articles_df, curr_article], ignore_index=True)

articles_df.to_csv('articles.csv')
print(articles_found)