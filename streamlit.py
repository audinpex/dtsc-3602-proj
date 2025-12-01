# fraud_dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
from textblob import TextBlob

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Fraud Article Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🔍 Fraud Article Analysis Dashboard")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("fraud_articles_summarized.csv")
    # Fill NaN to avoid errors
    df['keywords_found'] = df['keywords_found'].fillna('')
    df['summary'] = df['summary'].fillna('')
    return df

df = load_data()
st.sidebar.header("Filters")

# --- FILTERS ---
trend_options = ['All'] + sorted(df['trend'].dropna().unique().tolist())
selected_trend = st.sidebar.selectbox("Select Fraud Trend", trend_options)

keyword_options = ['All'] + sorted(set([kw.strip() for kws in df['keywords_found'] for kw in kws.split(',') if kw]))
selected_keyword = st.sidebar.selectbox("Select Keyword", keyword_options)

filtered_df = df.copy()
if selected_trend != 'All':
    filtered_df = filtered_df[filtered_df['trend'] == selected_trend]
if selected_keyword != 'All':
    filtered_df = filtered_df[filtered_df['keywords_found'].str.contains(selected_keyword, case=False)]

st.markdown(f"### Showing {len(filtered_df)} articles")

# --- DATA TABLE ---
with st.expander("View Data Table"):
    st.dataframe(filtered_df[['title', 'author', 'url', 'keywords_found', 'trend', 'summary', 'sentiment']])

# --- TOP KEYWORDS ---
st.subheader("Top 5 Fraud-Related Keywords")
all_keywords = [kw.strip().lower() for item in filtered_df['keywords_found'] for kw in item.split(',') if kw]
keyword_counts = Counter(all_keywords)
top5 = keyword_counts.most_common(5)

fig, ax = plt.subplots()
ax.bar([k for k, _ in top5], [v for _, v in top5], color='skyblue')
ax.set_xlabel("Keyword")
ax.set_ylabel("Frequency")
ax.set_title("Top 5 Keywords")
st.pyplot(fig)

# --- FRAUD TRENDS ---
st.subheader("Fraud Trend Distribution")
trend_counts = filtered_df['trend'].value_counts()
fig2, ax2 = plt.subplots()
trend_counts.plot(kind='bar', color='steelblue', ax=ax2)
ax2.set_ylabel("Number of Articles")
ax2.set_title("Top Fraud Trends")
st.pyplot(fig2)

# --- WORDCLOUD ---
st.subheader("WordCloud of Summaries")
text_all = " ".join(filtered_df['summary'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_all)

fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.imshow(wordcloud, interpolation='bilinear')
ax3.axis("off")
st.pyplot(fig3)

# --- SENTIMENT DISTRIBUTION ---
st.subheader("Sentiment Analysis of Summaries")
filtered_df['sentiment'] = filtered_df['summary'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)

fig4, ax4 = plt.subplots()
ax4.hist(filtered_df['sentiment'], bins=10, color='orange', edgecolor='black')
ax4.set_xlabel("Polarity (–1 = Negative, +1 = Positive)")
ax4.set_ylabel("Count")
ax4.set_title("Sentiment Distribution")
st.pyplot(fig4)

# --- INTERACTIVE ARTICLE VIEW ---
st.subheader("Read Articles")
article_titles = filtered_df['title'].tolist()
selected_article = st.selectbox("Select an Article", article_titles)

if selected_article:
    article_row = filtered_df[filtered_df['title'] == selected_article].iloc[0]
    st.markdown(f"**Author:** {article_row['author']}")
    st.markdown(f"**URL:** [Link]({article_row['url']})")
    st.markdown(f"**Keywords Found:** {article_row['keywords_found']}")
    st.markdown(f"**Trend:** {article_row['trend']}")
    st.markdown(f"**Summary:** {article_row['summary']}")
    st.markdown(f"**Full Text:** {article_row['text'][:1000]}...")  # show first 1000 chars

st.sidebar.markdown("---")
st.sidebar.markdown("Dashboard built with Streamlit")
