#import flask 
from flask import Flask, request, render_template
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key="20aa9cbb2d4d4735a0d27202348e50c7")

app = Flask(__name__)

def find_sources_and_domains():
    all_sources = newsapi.get_sources()['sources']
    sources = []
    domains = []
    for source in all_sources:
        id = source['id']
        domain = source['url'].replace("http://", "")
        domain = domain.replace("https://", "")
        domain = domain.replace("www.", "")
        slash = domain.find('/')
        if slash != -1:
            domain = domain[:slash]
        sources.append(id)
        domains.append(domain)
    sources = ", ".join(sources)
    domains = ", ".join(domains)
    return sources, domains 

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        sources, domains = find_sources_and_domains()
        search = request.form['search']
        all_news = newsapi.get_everything(
            q=search, 
            sort_by='relevancy',
            language='en', 
            sources=sources, 
            domains=domains
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
            from_param='2022-10-24',
            to='2022-11-01',
            sources=sources, 
            domains=domains,
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
