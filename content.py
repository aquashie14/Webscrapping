from bs4 import BeautifulSoup
import requests
from pathlib import Path
import time
from typing import List, Dict
import json

def read_urls(filename: str) -> List[str]:
    urls = []
    with open(filename) as f:
        for line in f:
            if line.startswith('URL'):
                urls.append(line.lstrip('URL :').strip())
    return urls

def scrape_url(url: str) -> Dict:
    time.sleep(1)  # Basic rate limiting
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "No title"
        
        content = []
        for elem in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a']):
            if elem.get_text(strip=True):
                content.append({
                    'type': 'heading' if elem.name.startswith('h') else 'paragraph',
                    'text': elem.get_text(strip=True)
                })
        
        return {
            'url': url,
            'title': title,
            'content': content,
            'status': 'success'
        }
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return {
            'url': url,
            'status': 'error',
            'error': str(e)
        }

def save_results(results: List[Dict], output_dir: str):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Save JSON
    with open(output_dir / 'content.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    # Save TXT
    with open(output_dir / 'content.txt', 'w', encoding='utf-8') as f:
        for result in results:
            if result['status'] == 'success':
                f.write(f"\nURL: {result['url']}\n")
                f.write(f"Title: {result['title']}\n")
                for item in result['content']:
                    f.write(f"{item['text']}\n")
                f.write("-" * 80 + "\n")

def main():
    urls = read_urls('webpages.txt')
    results = [scrape_url(url) for url in urls]
    save_results(results, 'scraped_content')

if __name__ == "__main__":
    main()