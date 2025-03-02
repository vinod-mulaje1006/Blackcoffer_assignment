# Blackcoffer_assignment
Web_scraping_and_text_analysis

Overview

This project consists of two Python scripts:

scrapping.py – A web scraping script that extracts structured data from web pages.

text_analysis.py – A text processing and sentiment analysis script that cleans, tokenizes, and analyzes text data.

Features

✅ Scrapes web content using BeautifulSoup✅ Extracts structured data such as Title, Problem Statement, Solution, and Tech Stack✅ Performs text preprocessing (tokenization, stopword removal, and sentiment analysis)✅ Calculates various readability metrics such as Fog Index and Average Sentence Length✅ Outputs cleaned text data and analysis results to CSV files

Dependencies

Install the required Python packages using:

pip install -r requirements.txt

Required Libraries:

pandas

requests

beautifulsoup4

nltk

textblob

re

json

Usage

Step 1: Web Scraping

Run the scraping script to extract data from URLs:

python scrapping.py

This will create JSON files containing structured data for each webpage.

Step 2: Text Analysis

Run the text analysis script to process the extracted text:

python text_analysis.py

The output will be saved as Output_Data.csv.

