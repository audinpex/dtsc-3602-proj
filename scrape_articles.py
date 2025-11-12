import bs4
import requests
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt_tab')

# --- FRAUD KEYWORDS ---
FRAUD_KEYWORDS = [
    'embezzlement', 'bribery', 'fraud investigation', 'money laundering', 'scam'
]

# --- LOAD URLS ---
with open("article_urls.txt", 'r', encoding='utf-8') as f:
    urls = [line.strip() for line in f if line.strip()]

# --- CREATE DATAFRAME ---
articles_df = pd.DataFrame(columns=['title', 'author', 'url', 'text', 'keywords_found', 'summary'])

articles_found = 0

# --- SCRAPE, DETECT, SUMMARIZE ---
for i, current_url in enumerate(urls[:250]):
    try:
        raw_article = requests.get(current_url, timeout=10)
        raw_article.raise_for_status()
        souped_article = bs4.BeautifulSoup(raw_article.text, 'html.parser')

        article_title = souped_article.find('h1')
        article_author = souped_article.find('h5', class_='margin-top-1')
        article_body = souped_article.find('div', class_='cell large-8')

        if not article_title or not article_body:
            print(f"Skipping (missing content): {current_url}")
            continue

        title = article_title.get_text(strip=True)
        author = article_author.get_text(strip=True) if article_author else "Unknown"
        body_text = article_body.get_text(separator=' ', strip=True)
        body_lower = body_text.lower()

        # --- FRAUD DETECTION ---
        found_keywords = [kw for kw in FRAUD_KEYWORDS if kw.lower() in body_lower]

        if found_keywords:
            articles_found += 1

            # --- SIMPLE SUMMARIZATION ---
            sentences = sent_tokenize(body_text)
            summary_sentences = []
            for sent in sentences:
                if any(kw in sent.lower() for kw in found_keywords):
                    summary_sentences.append(sent)
            # Combine 2–3 keyword-heavy sentences as summary
            summary = " ".join(summary_sentences[:3])
            if not summary:
                summary = body_text[:300] + "..."

            # --- STORE ---
            articles_df.loc[len(articles_df)] = {
                'title': title,
                'author': author,
                'url': current_url,
                'text': body_text,
                'keywords_found': ', '.join(found_keywords),
                'summary': summary
            }

        print(f"Processed ({i+1}/{len(urls)}): {title[:60]}...")

    except Exception as e:
        print(f"Error scraping {current_url}: {e}")

# --- SAVE RESULTS ---
articles_df.to_csv('fraud_articles_summarized.csv', index=False, encoding='utf-8')
print(f"\n✅ Found {articles_found} fraud-related articles.")
print("💾 Saved as fraud_articles_summarized.csv")