import requests
from bs4 import BeautifulSoup
import time
import random
import json

def get_user_agent():
    """Return a random user agent to avoid detection."""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    ]
    return random.choice(user_agents)

def scrape_studocu(url):
    """Scrape content from StudoSu."""
    headers = {
        'User-Agent': get_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        print(f"Fetching URL: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title
        title = soup.find('h1', class_='document-title')
        title_text = title.text.strip() if title else "Title not found"
        
        # Extract document content
        document_content = soup.find('div', class_='page-content-wrapper')
        
        # Extract text from paragraphs
        paragraphs = []
        if document_content:
            for p in document_content.find_all(['p', 'div', 'span']):
                if p.text.strip():
                    paragraphs.append(p.text.strip())
        
        # Extract metadata
        metadata = {}
        meta_section = soup.find('div', class_='document-info')
        if meta_section:
            for item in meta_section.find_all('div', class_='info-row'):
                label = item.find('div', class_='label')
                value = item.find('div', class_='value')
                if label and value:
                    metadata[label.text.strip()] = value.text.strip()
        
        # Compile results
        results = {
            'title': title_text,
            'url': url,
            'metadata': metadata,
            'content': paragraphs[:100]  # Limit to first 100 paragraphs for brevity
        }
        
        return results
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None
    except Exception as e:
        print(f"Error parsing content: {e}")
        return None

def save_to_file(data, filename="studocu_data.json"):
    """Save scraped data to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Data saved to {filename}")

def main():
    url = "https://www.studocu.com/en-au/document/university-of-melbourne/principles-of-finance/final-notes-1-12-lecture-notes/9905556?origin=course-highest-rated-1"
    
    print("Starting scraper...")
    data = scrape_studocu(url)
    
    if data:
        print(f"Successfully scraped: {data['title']}")
        save_to_file(data)
        
        # Print a sample of the content
        print("\nSample content:")
        for i, para in enumerate(data['content'][:5]):
            print(f"{i+1}. {para[:100]}...")
    else:
        print("Failed to scrape data.")

if __name__ == "__main__":
    main()

def scrape_subject_page(url):
    """
    Scrape a subject page and return the data as JSON.
    
    Args:
        url (str or list): URL or list of URLs to scrape
        
    Returns:
        str: JSON string of the scraped data
    """
    try:
        # Handle case where url might be None
        if not url:
            return json.dumps({"error": "No URL provided"})
            
        data = scrape_studocu(url)
        
        if data:
            return json.dumps(data)
        else:
            return json.dumps({"error": "Failed to scrape data from URL"})
    except Exception as e:
        print(f"Error in scrape_subject_page: {str(e)}")
        return json.dumps({"error": f"Error scraping page: {str(e)}"})


