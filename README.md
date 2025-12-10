# dtsc-3602-proj
Fraud Article Scraping & Analysis Pipeline
A Data-Driven Fraud Detection & Trend Analysis Project — DTSC 3602

Team 11
Team Lead: Alexi McNabb
Storyteller / Communication Lead: Aaron Foley
Data Analyst: Will Jones
Domain Expert: Chase Patterson

Project Overview
This project builds a complete, automated pipeline that scrapes fraud-related articles from the ACFE Insights Blog, classifies them using fraud-specific keywords, stores structured datasets, and generates sentiment + keyword analyses along with visual summaries of emerging fraud trends.
The pipeline supports scraping → filtering → storing → analyzing → visualizing.

Quick Start
Install Dependencies
uv venv
uv pip install -r requirements.txt

Environment Setup
Create a .env file in the project root:
SUPABASE_URL=your_url
SUPABASE_KEY=your_service_role_key

Run the Pipeline
python src/pipeline.py

Run Individual Components
Scraper: python src/scraper.py
Keyword Filter: python src/filter_keywords.py


Methodology
1. Scrape
Uses requests + BeautifulSoup to pull article titles, text, URLs, and metadata from the ACFE Insights Blog.
2. Filter
Articles are flagged as fraud-related using a refined keyword list, including: fraud, scam, embezzlement, whistleblower, bribery, corruption, money laundering, racketeering, non-compliance, irregularity
3. Store
Data is saved in: Pandas DataFrame, CSV (articles.csv), Supabase table (fraud_articles)
4. Analyze
Pipeline computes: Keyword frequency, Category classification (Financial vs. General Fraud), Trend summaries.
5. Visualize: Word Cloud, Keyword Frequency Histogram, Fraud Category Distribution Chart, Sentiment Histogram, All results are saved in /outputs.

Dataset Summary
Top 5 Fraud-Related Terms: Scam, Embezzlement, Fraud Investigation, Money Laundering, Bribery
Analysis: Most articles scored neutral to slightly positive, consistent with factual reporting. Negative articles typically involved severe corporate fraud or high-loss events.

Key Findings
Top Fraud Trends: Rise in scam-based fraud, especially phishing, text scams, and consumer-targeted schemes. Corporate & internal fraud (embezzlement, bribery, laundering) remains consistently represented. Consumer fraud dominates, indicating widespread everyday risk among the general public.

Technologies Used
Python: BeautifulSoup, Requests, Pandas
Supabase: Backend storage
NLTK / TextBlob: Sentiment scoring
Matplotlib, WordCloud: Visual analytics
Git & GitHub: Version control

Deliverables
Complete scraped dataset (CSV + Supabase)
Keyword-classified dataset
Sentiment summary + statistical analysis
Visualizations folder
Presentation slide deck
Fully documented codebase
