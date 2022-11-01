#import flask 
from flask import Flask, request, render_template
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key="20aa9cbb2d4d4735a0d27202348e50c7")

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        search = request.form['search']
        all_news = newsapi.get_everything(
            q=search, 
            language='en'
        )

        #limit amount of articles available 
        amount_of_articles = all_news['totalResults']
        if amount_of_articles > 100:
            amount_of_articles = 100

        #article section 
        all_articles = newsapi.get_everything(
            q=search, 
            language='en',
            sort_by='relevancy',
            page_size=amount_of_articles
        )['articles']
        return render_template('index.html', all_articles=all_articles, search=search)
    else:
            #get top headlines 
            top_headlines = newsapi.get_top_headlines(language='en')
            total_results = top_headlines['totalResults']
            if total_results > 100:
                total_results = 100
                all_headlines = newsapi.get_top_headlines(
                                                     page_size=total_results)['articles']
                return render_template("index.html", all_headlines = all_headlines)
            return render_template('index.html')

if __name__ == '__main__':
    app.run()