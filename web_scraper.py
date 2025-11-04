# This is the code for web_scraper.py

import requests
from bs4 import BeautifulSoup

# The URL of the blog we are going to scrape
URL_TO_SCRAPE = "https://blog.langchain.com/"

def scrape_latest_langchain_news():
    """
    Scrapes the LangChain blog for the titles of the latest articles.
    This acts as our "Web-Scraper Agent".
    """
    print("Web-Scraper Agent: Fetching latest news from LangChain blog...")
    
    try:
        # Set a User-Agent header to pretend we are a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        # 1. Fetch the webpage
        response = requests.get(URL_TO_SCRAPE, headers=headers, timeout=10)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Web-Scraper Agent: Failed to get page, status code {response.status_code}")
            return None

        # 2. Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 3. Find the article titles
        # This part is fragile and depends on the website's structure.
        # As of now, LangChain blog posts seem to use <h2> tags with a specific class.
        # We'll just look for <h2> tags to keep it simple.
        article_titles = []
        
        # Find all <h2> tags, which are typically used for headings
        for title in soup.find_all('h2', limit=5): # Get the first 5
            article_titles.append(title.get_text(strip=True))

        if not article_titles:
            print("Web-Scraper Agent: Could not find any article titles.")
            return None
            
        # 4. Format the titles into a single string
        scraped_data = "Here are the latest headlines from the LangChain blog: \n"
        scraped_data += "\n - ".join(article_titles)
        
        print("Web-Scraper Agent: Successfully scraped data.")
        return scraped_data

    except Exception as e:
        print(f"Web-Scraper Agent: Error during scraping - {e}")
        return None

# This is for testing. If you run "python web_scraper.py", it will test the function.
if __name__ == "__main__":
    news = scrape_latest_langchain_news()
    if news:
        print("\n--- SCRAPED DATA ---")
        print(news)
    else:
        print("Scraping failed.")