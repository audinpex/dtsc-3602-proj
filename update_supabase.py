import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
from supabase import create_client, client
import json
import csv

load_dotenv()
articles_pd = pd.read_csv("fraud_articles_summarized.csv")
articles_pd.to_json('articles_summarized.json')

with open('articles_summarized.json') as articles_in:
    articles_in2 = json.load(articles_in)
articles_df = pd.DataFrame(articles_in2)

DATABASE_URL = os.getenv("SUPABASE_URL")
if not DATABASE_URL:
    print("URL not found")
    exit

def init_connection():
    url = DATABASE_URL
    key = os.getenv("SUPABASE_KEY")
    return create_client(url, key)
supabaser = init_connection()

for row in articles_df.index:
    response = (supabaser.table('articles_summarized').upsert(articles_df.loc[row].to_dict()).execute())