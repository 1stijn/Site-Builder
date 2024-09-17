import random
from collections import defaultdict
import time

def get_page_from_keywords(keywords_list, query):
    query = query.lower()
    
    page_scores = defaultdict(int)
    
    for page, keywords in keywords_list.items():
        for keyword in keywords:
            page_scores[page] += query.count(keyword)
    
    if page_scores:
        best_page = max(page_scores, key=page_scores.get)
        return best_page
    return 'No matching page found'

def generate_description():
    descriptions = [
    ]
    
    return random.choice(descriptions)

def log_results(description, page):
    with open("query_log.txt", "a") as file:
        file.write(f"Description: {description}\n")
        file.write(f"Recommended Page: {page}\n")
        file.write("-" * 40 + "\n")

keywords = {
}

while True:
    description = generate_description()
    print(f"Generated Description: {description}")

    page = get_page_from_keywords(keywords, description)
    print(f"Recommended Page: {page}")

    log_results(description, page)