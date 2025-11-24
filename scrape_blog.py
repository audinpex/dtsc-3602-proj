import bs4
import requests
import os

# Gets html of main blog page
blog_scrape = "https://www.acfe.com/acfe-insights-blog"
raw_blog = requests.get(blog_scrape)
soup_blog = bs4.BeautifulSoup(raw_blog.text, 'html.parser')

with open("acfe_blog.txt", 'w', encoding='utf-8') as f:
    f.write(str(soup_blog))

# Identifies links to blog articles and writes them to a text file
articles = soup_blog.find_all("a", class_='color-secondary')
article_links = ""
for article in articles:
    link = article.get('href')
    article_links += link + "\n"
with open("article_urls.txt", 'w', encoding='utf-8') as f:
    f.write(str(article_links))