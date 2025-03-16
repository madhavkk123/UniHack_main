from bs4 import BeautifulSoup
import requests
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import traceback

def get_subject_page_url(query):
    """
    Given a user query (e.g., "principles of finance uni melb"),
    build the search URL, parse the search results, and attempt
    to find the best matching page link.
    
    Args:
        query (str): The search query
        
    Returns:
        list: List of URLs found, or None if no results
    """
    try:
        options = Options()
        options.headless = True  # Run in headless mode (no browser UI)
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Initialize the driver (make sure you have the matching ChromeDriver installed)
        driver = webdriver.Chrome(options=options)
        
        url = f"https://www.studocu.com/en/search?query={query}"
        driver.get(url)

        # Give the page a few seconds to load JS and bypass any challenge
        time.sleep(5)

        # Get the rendered HTML
        html = driver.page_source
        driver.quit()

        # Parse the HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract <a> tags
        results_div = soup.find_all("div", {"class": "DocumentCardRich_header__8ueqN"})
        list_of_links = []
        
        # Extract the href attribute from each <a> tag
        if results_div:
            for div in results_div:
                a_tag = div.find("a")
                if a_tag and a_tag.get("href"):
                    search_links = a_tag.get("href")
                    new_url = "https://www.studocu.com" + search_links
                    list_of_links.append(new_url)
                    
        if not list_of_links:
            print("No links found for query:", query)
            return None
        elif len(list_of_links) <= 10:
            return list_of_links
        else:
            return list_of_links[:10]
            
    except Exception as e:
        print(f"Error in get_subject_page_url: {str(e)}")
        print(traceback.format_exc())
        return None

if __name__ == "__main__":
    user_input = "principles of finance uni melb"
    highest_rated_url = get_subject_page_url(user_input)
    print(highest_rated_url)