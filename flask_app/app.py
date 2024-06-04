from flask import Flask, request, render_template, redirect, url_for
import requests
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongo', 27017)
db = client.realestate
collection = db.data
search_history = db.search_history

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    price_min = request.form.get('priceMin')
    price_max = request.form.get('priceMax')
    count = request.form.get('count')
    requests.post('http://scraper:5001/start_scraping', json={'price_min': price_min, 'price_max': price_max, 'count':count})
    return redirect(url_for('scraping_started'))

@app.route('/scraping_started')
def scraping_started():
    return render_template('scraping_started.html')

@app.route('/results')
def results():
    data = list(collection.find())
    return render_template('results.html', data=data)

@app.route('/history')
def history():
    search_data = list(search_history.find())
    return render_template('history.html', search_data=search_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
