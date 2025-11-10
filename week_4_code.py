import pandas as pd
df = pd.read_csv("fraud_articles_summarized.csv")
print(df.head())
print(f"Total fraud-related articles: {len(df)}")

######

from collections import Counter
import matplotlib.pyplot as plt

# Split and count all keywords
all_keywords = []
for item in df['keywords_found'].dropna():
    all_keywords.extend([kw.strip().lower() for kw in item.split(',')])

keyword_counts = Counter(all_keywords)
top5 = keyword_counts.most_common(5)
print("Top 5 Keywords:", top5)

# Plot
plt.bar([k for k, _ in top5], [v for _, v in top5])
plt.title("Top 5 Fraud-Related Keywords")
plt.xlabel("Keyword")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()


#########


def classify_trend(keywords):
    k = keywords.lower()
    if any(x in k for x in ['phishing', 'cybercrime', 'data breach', 'ransomware']):
        return 'Cyber Fraud'
    elif any(x in k for x in ['embezzlement', 'corruption', 'money laundering']):
        return 'Financial Fraud'
    elif any(x in k for x in ['non-compliance', 'error', 'irregularity']):
        return 'Compliance Issues'
    else:
        return 'Other'

df['trend'] = df['keywords_found'].fillna('').apply(classify_trend)
trend_counts = df['trend'].value_counts()
print(trend_counts)

trend_counts.plot(kind='bar', color='steelblue', title='Top Fraud Trends')
plt.ylabel("Number of Articles")
plt.tight_layout()
plt.show()


########

from wordcloud import WordCloud

text_all = " ".join(df['summary'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_all)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Common Words in Fraud Summaries")
plt.show()


######

from textblob import TextBlob

df['sentiment'] = df['summary'].dropna().apply(lambda x: TextBlob(str(x)).sentiment.polarity)
print(df['sentiment'].describe())

plt.hist(df['sentiment'], bins=10, color='orange', edgecolor='black')
plt.title("Sentiment Distribution of Fraud Summaries")
plt.xlabel("Polarity (–1 = Negative, +1 = Positive)")
plt.ylabel("Count")
plt.show()

