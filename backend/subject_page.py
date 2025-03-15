import requests
from bs4 import BeautifulSoup

def get_subject_page_url(query, session=None):
    """
    Given a user query (e.g., "principles of finance uni melb"),
    build the search URL, parse the search results, and attempt
    to find the best matching page link.
    """
    base_search_url = f"https://www.studocu.com/en/search?query={query}"
    return base_search_url

if __name__ == "__main__":
    user_input = "principles of finance uni melb"
    highest_rated_url = get_subject_page_url(user_input)
