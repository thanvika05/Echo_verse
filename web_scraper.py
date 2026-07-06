import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, Any
from urllib.parse import urlparse
import time
from config import Config

class WebScraper:
    """Handles web scraping and content extraction from various websites"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': Config.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def extract_text_from_url(self, url: str) -> Dict[str, Any]:
        """Extract text content from a given URL"""
        try:
            # Validate URL
            if not self._is_valid_url(url):
                raise ValueError("Invalid URL format")
            
            # Fetch the webpage
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract content based on website type
            content = self._extract_content(soup, url)
            
            # Clean and process the content
            cleaned_content = self._clean_content(content['text'])
            
            return {
                'url': url,
                'title': content['title'],
                'text': cleaned_content,
                'word_count': len(cleaned_content.split()),
                'char_count': len(cleaned_content),
                'domain': urlparse(url).netloc,
                'status': 'success'
            }
            
        except requests.RequestException as e:
            return {
                'url': url,
                'error': f"Failed to fetch URL: {str(e)}",
                'status': 'error'
            }
        except Exception as e:
            return {
                'url': url,
                'error': f"Error processing URL: {str(e)}",
                'status': 'error'
            }
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _extract_content(self, soup: BeautifulSoup, url: str) -> Dict[str, str]:
        """Extract content from HTML soup based on website type"""
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe']):
            element.decompose()
        
        # Try to find the main content area
        content_selectors = [
            'article',
            '[role="main"]',
            '.content',
            '.post-content',
            '.entry-content',
            '.article-content',
            'main',
            '.main-content'
        ]
        
        main_content = None
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if not main_content:
            # Fallback to body content
            main_content = soup.find('body')
        
        # Extract title
        title = self._extract_title(soup)
        
        # Extract text from main content
        if main_content:
            text = main_content.get_text(separator='\n', strip=True)
        else:
            text = soup.get_text(separator='\n', strip=True)
        
        return {
            'title': title,
            'text': text
        }
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        # Try different title selectors
        title_selectors = [
            'h1',
            '.title',
            '.post-title',
            '.article-title',
            'title'
        ]
        
        for selector in title_selectors:
            title_element = soup.select_one(selector)
            if title_element:
                title = title_element.get_text(strip=True)
                if title and len(title) > 10:  # Ensure it's a meaningful title
                    return title
        
        # Fallback to page title
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text(strip=True)
        
        return "Untitled"
    
    def _clean_content(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common web artifacts
        text = re.sub(r'Share this|Tweet|Like|Follow|Subscribe', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Cookie|Privacy|Terms|Contact', '', text, flags=re.IGNORECASE)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove multiple newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text.strip()
