from flask import Flask, request
import multiprocessing
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from pymongo import MongoClient

app = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

client = MongoClient('mongo', 27017)
db = client.realestate
collection = db.data
search_history = db.search_history

def get_page_content(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 403:
            print('Access forbidden. Status code: 403')
        else:
            print(f'Failed to retrieve the page. Status code: {response.status_code}')
    except Exception as e:
        print(f'Error occurred while fetching the page: {e}')
    return None

def extract_links_from_page(url):
    content = get_page_content(url)
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.find_all('a', {'data-cy': 'listing-item-link'})
        base_url = 'https://www.otodom.pl'
        return [urljoin(base_url, link['href']) for link in links]
    else:
        return []

def extract_all_links(base_url, count):
    all_links = []
    for page_num in range(1, 100):
        if len(all_links) >= int(count) : return all_links[:int(count)]
        page_url = f"{base_url}&page={page_num}"
        links = extract_links_from_page(page_url)
        all_links.extend(links)
    return all_links[:int(count)]

def extract_information(url):
    
    content = get_page_content(url)
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        price_tag = soup.find('strong', {'aria-label': 'Cena'})
        price_per_meter_tag = soup.find('div', {'aria-label': 'Cena za metr kwadratowy'})
        area_tag = soup.find('div', {'data-testid': 'table-value-area'})
        rooms_tag = soup.find('div', {'aria-label': 'Liczba pokoi'})
        floor_tag = soup.find('div', {'aria-label': 'Piętro'})

        price = price_tag.get_text(strip=True) if price_tag else 'Brak ceny'
        price_per_meter = price_per_meter_tag.get_text(strip=True) if price_per_meter_tag else 'Brak ceny za metr kwadratowy'
        area = area_tag.get_text(strip=True) if area_tag else 'Brak powierzchni'
        rooms = rooms_tag.get_text(strip=True) if rooms_tag else 'Brak informacji o liczbie pokoi'
        floor = floor_tag.get_text(strip=True) if floor_tag else 'Brak informacji o piętrze'

        scraped = {
            "url": url,
            "price": price,
            "price_per_meter": price_per_meter,
            "area": area,
            "rooms": rooms[-1],
            "floor": floor.replace("Piętro", "", 1).capitalize().strip()
        }
        collection.insert_one(scraped)
    else:
        return None

def main(price_min, price_max,count):
    base_url = f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/cala-polska?limit=36&ownerTypeSingleSelect=ALL&pricePerMeterMin={price_min}&pricePerMeterMax={price_max}&by=DEFAULT&direction=DESC&viewType=listing"
    collection_to_drop = db.data
    collection_to_drop.drop()
    
    all_links = extract_all_links(base_url,count)
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.map(extract_information, all_links)
    search = {
        "price_min": price_min,
        "price_max": price_max,
        "count": count,
        "date": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    search_history.insert_one(search)

    

@app.route('/start_scraping', methods=['POST'])
def start_scraping():
    data = request.get_json()
    price_min = data['price_min']
    price_max = data['price_max']
    count = data['count']
    if count == '':
        count ='20'
    main(price_min, price_max,count)
    return "Scraping completed!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
