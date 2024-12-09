# -*- coding: utf-8 -*-
"""GDELT News Extractor.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1S8UXew1vlL2UvNeR7ztESkmhHMzQNbEn
"""

!pip install gdeltdoc
!pip install newspaper4k

from gdeltdoc import GdeltDoc, Filters
from tqdm import tqdm
import newspaper
import pandas as pd

f = Filters(
    keyword = "trump",
    start_date = "2020-02-01",
    end_date = "2020-02-02",
    num_records = 250,
    domain="foxnews.com",
    country = "US",
)

gd = GdeltDoc()
# Search for articles matching the filters
articles = gd.article_search(f)


main_text_rquired=0


if main_text_rquired:
  # Initialize main_text column as empty
  articles['main_text'] = ""
  for i in tqdm(range(len(articles))):
      url = articles.iloc[i]['url']
      try:
          # Check if URL is not empty or null
          if pd.notnull(url):
              news_paper = newspaper.article(url)
              articles.at[i, 'main_text'] = news_paper.text
          else:
              articles.at[i, 'main_text'] = "Invalid URL"
      except Exception as e:
          # Handle errors in downloading or parsing the article
          articles.at[i, 'main_text'] = f"Error: {str(e)}"