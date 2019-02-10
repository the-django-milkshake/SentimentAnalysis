from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
from langdetect import detect

class Analysis():
    def __init__(self, term):
        self.term = term
        self.subjectivity = 0
        self.sentiment = 0

        self.url = 'https://www.google.com/search?q={0}&source=lnms&tbm=nws'.format(self.term)

    def run(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        headline_results = soup.find_all('div', class_='st')
        headline_papers = soup.find_all('div', class_='slp')

        newsanalysis = []

        for h,p in zip(headline_results, headline_papers):
            blob = TextBlob(h.get_text())
            lang = detect(h.get_text())
            if lang != "en":
                continue
            head = p.get_text()
            senti = blob.sentiment.polarity
            sub = blob.sentiment.subjectivity
            self.sentiment += senti / len(headline_results)
            self.subjectivity += sub / len(headline_results)
            newsanalysis.append({'blob':blob, 'text':h.get_text(), 'source':head, 'subjectivity': sub, 'sentiment': senti})
        return newsanalysis