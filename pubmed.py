

from Bio import Entrez
import datetime
import re
import json

def save_data(papers, filename='data/papers_data.json'):
    formatted_papers = []
    for paper in papers:
        article = paper['MedlineCitation']['Article']
        authors = article.get('AuthorList', [])
        formatted_authors = []
        for author in authors:
            forename = author.get('ForeName', '')
            lastname = author.get('LastName', '')
            full_name = ' '.join([forename, lastname]).strip()
            if full_name:  # Only add if the author's name is not empty
                formatted_authors.append(full_name)

        paper_data = {
            'title': article.get('ArticleTitle'),
            'abstract': article['Abstract']['AbstractText'][0] if 'Abstract' in article else 'No abstract available',
            'authors': formatted_authors,
            'pub_date': article['Journal']['JournalIssue']['PubDate'],
            'pmid': paper['MedlineCitation']['PMID'],
            'pmcid': paper.get('PubmedData', {}).get('ArticleIdList', [])
        }
        formatted_papers.append(paper_data)

    # Save to a JSON file
    with open(filename, 'w') as f:
        json.dump(formatted_papers, f, indent=4)

def clean_text(text):
    # Remove special characters and extra whitespaces
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def search(query, start_year=2001):
    Entrez.email = 'lt89715@student.uni-lj.si'
    current_year = datetime.datetime.now().year
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='5000',
                            retmode='xml',
                            term=query,
                            mindate=f"{start_year}/01/01",
                            maxdate=f"{current_year}/12/31")
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'your_email@example.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    papers_with_pmcid = []
    for paper in results['PubmedArticle']:
        pmcids = [article_id for article_id in paper['PubmedData']['ArticleIdList'] if str(article_id).startswith('PMC')]
        if pmcids:
            # Only include the first PMCID (in case there are multiple)
            paper['PubmedData']['ArticleIdList'] = pmcids[0] 
            papers_with_pmcid.append(paper)
    return papers_with_pmcid

# Example usage
query = 'dictyostelium discoideum'
results = search(query)
id_list = results['IdList']
papers = fetch_details(id_list)

save_data(papers)

print(f"Found {len(papers)} papers with PMCID.")