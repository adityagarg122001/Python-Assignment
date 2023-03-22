import requests
from bs4 import BeautifulSoup
import time

# Scrape product details from a single page
def scrape_page(url):
    # Send a GET request to the given URL
    response = requests.get(url)
    
    # Wait for a few seconds to avoid overloading the server
    time.sleep(2)
    
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the product details
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    for product in products:
        try:
            # Extract the product URL, name, price, rating, and number of reviews
            product_url = product.find('a', {'class': 'a-link-normal s-no-outline'})['href']
            product_name = product.find('h2').text.strip()
            product_price = product.find('span', {'class': 'a-price-whole'}).text.strip()
            product_rating = product.find('span', {'class': 'a-icon-alt'}).text.strip()
            product_reviews = product.find('span', {'class': 'a-size-base'}).text.strip()

            # Print the product details
            print('Product URL:', product_url)
            print('Product Name:', product_name)
            print('Product Price:', product_price)
            print('Product Rating:', product_rating)
            print('Product Reviews:', product_reviews)
            
            # Scrape additional product details from the product URL
            scrape_product(product_url)
        except:
            continue

# Scrape product details from multiple pages
def scrape_pages(pages):
    for i in range(1, pages+1):
        url = f'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&page={i}'
        scrape_page(url)

# Scrape additional product details from a product URL
def scrape_product(url):
    # Send a GET request to the product URL
    response = requests.get(url)
    
    # Wait for a few seconds to avoid overloading the server
    time.sleep(2)
    
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the ASIN, product description, and manufacturer
    asin = soup.find('th', {'class': 'prodDetSectionEntry'}).text.strip()
    description = soup.find('div', {'id': 'productDescription'}).text.strip()
    manufacturer = soup.find('a', {'id': 'bylineInfo'}).text.strip()

    # Print the additional product details
    print('ASIN:', asin)
    print('Description:', description)
    print('Manufacturer:', manufacturer)

# Scrape 200 product URLs from the search results
scrape_pages(20)
