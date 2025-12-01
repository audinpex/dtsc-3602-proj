# dtsc-3602-proj
Fraud research project for DTSC-3602

Fraud Article Scraping & Analysis Project
Overview

This project focuses on scraping fraud-related articles from the ACFE Insights Blog, classifying them using targeted fraud-related keywords, storing the results in a structured dataset, and analyzing fraud trends through visualizations and statistical summaries.
The final pipeline automates scraping → filtering → storing → analyzing → visualizing.

This repository contains all code, documentation, images, and outputs created throughout the project.

📂 Project Structure
project/
│
├── data/                  # Raw and cleaned datasets (CSV, TXT, JSON)
├── outputs/               # Visualizations (PNG), statistical summaries
├── src/                   # All Python source code
│   ├── scraper.py         # Web scraping logic for ACFE blog
│   ├── filter_keywords.py # Keyword filtering and classification
│   ├── analysis.py        # Sentiment + statistical analysis
│   ├── supabase_upload.py # Code for sending scraped data to Supabase
│   └── pipeline.py        # Automated full workflow
│
├── images/                # Wordclouds, histograms, trend graphs
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

🛠️ Technologies Used

Python (BeautifulSoup, Requests, Pandas, Matplotlib)

Supabase (backend storage)

NLTK / TextBlob (sentiment scoring)

WordCloud (keyword visualization)

Git & GitHub (collaboration and version control)

🔍 Project Objectives

Scrape fraud-related articles from the ACFE Insights Blog.

Store scraped data in a structured format (pandas DataFrame, CSV, Supabase).

Classify articles using a refined set of fraud-related keywords.

Identify common themes and fraud trends.

Generate visualizations summarizing fraud activity.

Build a complete and reusable pipeline for future fraud analysis.

📑 Dataset Summary

After refining our keyword search to reduce noise, we collected 102 high-relevance articles using keywords such as:

Scam

Embezzlement

Fraud investigation

Bribery

Money laundering

Each article record includes:

Title

Full text

Matching keywords

Category (Financial / General Fraud)

Sentiment score

Metadata (URL, scrape date)

📊 Key Findings
1️⃣ Keyword Frequency

Top five fraud-related terms:

Scam

Embezzlement

Fraud Investigation

Money Laundering

Bribery

These dominated the narrative across ACFE posts.

2️⃣ Fraud Category Distribution

30% of articles → Financial Fraud (embezzlement, bribery, money laundering)

70% of articles → General or Other Fraud (phishing, identity theft, charity fraud, scams)

3️⃣ Sentiment Analysis

A histogram of polarity values revealed:

Most articles are neutral to slightly positive, due to factual reporting style

A smaller portion are negative, reflecting the severity of fraud cases

4️⃣ Emerging Trends

Rise in scam-based fraud (phishing, text scams).

Corporate and internal fraud remains consistently reported.

Consumer-level fraud dominates the "general fraud" category.

📈 Visualizations

Stored in /outputs or /images, including:

Word Cloud of most frequent terms

Keyword Frequency Histogram

Fraud Category Distribution Plot

Sentiment Distribution Histogram

Trend Breakdown Charts

Each image is automatically generated and saved during the pipeline run.

🧩 Pipeline Workflow
1. Scrape

Pulls ACFE articles using Requests + BeautifulSoup.

2. Filter

Identifies relevant articles using the refined keyword list.

3. Store

Saves data to:

pandas DataFrame

CSV files

Supabase database

4. Analyze

Calculates:

Keyword frequency

Sentiment polarity

Fraud categories

5. Visualize

Outputs multiple PNG charts for presentation use.

🚀 How to Run the Project
1. Install dependencies
pip install -r requirements.txt

2. Run the scraper
python src/scraper.py

3. Filter articles using keywords
python src/filter_keywords.py

4. Run full pipeline
python src/pipeline.py

📦 Deliverables

Complete scraped dataset (CSV + Supabase)

Keyword-classified dataset

Sentiment and statistical summaries

Visualizations (PNG)

Final report

Presentation slide deck

Full documented codebase

👥 Team Contributions

You can add a section like this:

Member A: Scraper development, keyword filtering

Member B: Data analysis, sentiment scoring, visualizations

Member C: Supabase integration, pipeline automation

Everyone: Documentation, testing, presentation

📨 Contact

For project questions or collaboration:
Team Name / Emails / GitHub Handles
