import requests
from bs4 import BeautifulSoup
import re
import json

def clean_text(text):
    # Remove content after acknowledging or references section
    if "Abstract" in text:
        text = text.split("Abstract")[1]
    if "ABSTRACT" in text:
        text = text.split("ABSTRACT")[1]
    text = text.split("Acknowledgments")[0]
    text = text.split("ACKNOWLEDGMENTS")[0]
    text = text.split("References")[0]
    text = text.split("REFERENCES")[0]
    # Remove URLs, references like [10][11], special characters, and unnecessary spaces
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\{.*?\}', '', text)
    text = re.sub(r'\s+', ' ', text)  # Normalize spaces
    text = re.sub(r'\s\.', '.', text)  # Remove space before period
    text = re.sub(r'\s,', ',', text)  # Remove space before comma

    # text = re.sub(r'[^A-Za-z0-9.,;:\s]+', ' ', text)
    # text = re.sub(r'\s+', ' ', text).strip()
    

    return text

def download_pubreader_text(pmcid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Fetch the main article page
    url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve article page for {pmcid}. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    pubreader_link = soup.find('a', class_='sidefm-pmclink')
    
    if not pubreader_link or 'href' not in pubreader_link.attrs:
        print(f"PubReader link not found for {pmcid}.")
        return

    pubreader_url = "https://www.ncbi.nlm.nih.gov" + pubreader_link['href']
    
    # Fetch the PubReader content
    pubreader_response = requests.get(pubreader_url, headers=headers)
    if pubreader_response.status_code == 200:
        soup = BeautifulSoup(pubreader_response.content, 'html.parser')
        article_text = soup.get_text(separator=' ', strip=True)
        article_text = clean_text(article_text)
        # Save the article text to a file
        with open(f"data/{pmcid}.txt", 'w', encoding='utf-8') as file:
            file.write(article_text)
        print(f"Saved text for {pmcid}.")
    else:
        print(f"Failed to download PubReader content for {pmcid}. Status code: {pubreader_response.status_code}")


def download_articles(pmcid_list, folder_path="data/"):
    for pmcid in pmcid_list:
        download_pubreader_text(pmcid)

# Load PMCIDs from JSON file
with open('papers_data.json', 'r') as f:
    papers_data = json.load(f)

def download_articles_from_json(json_file, folder_path="data/"):
    # Load PMCIDs from JSON file
    with open(json_file, 'r') as f:
        papers_data = json.load(f)

    # Extract PMCIDs from papers_data
    pmcid_list = [paper['pmcid'] for paper in papers_data if 'pmcid' in paper]

    # Download articles
    for pmcid in pmcid_list:
        download_pubreader_text(pmcid)

# Example usage
download_articles_from_json('papers_data.json')