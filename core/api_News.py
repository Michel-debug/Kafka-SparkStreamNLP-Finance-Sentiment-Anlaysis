from newsapi import NewsApiClient
import requests
def fetch_financial_news_seekingalpha():
    
    url = "https://seeking-alpha.p.rapidapi.com/news/v2/list"

    querystring = {"category":"market-news::financials","size":"40"}
    
    headers = {
        "X-RapidAPI-Key": "e3ffde7ad0msh33323e10f821f13p15885bjsn25fc84293c2a",
        "X-RapidAPI-Host": "seeking-alpha.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


def fetch_bbc_news():
    # Init
    newsapi = NewsApiClient(api_key='e20960921b7c4bc7ad4fd59ea6537d45')

    # /v2/top-headlines
    top_headlines = newsapi.get_top_headlines(q='finance',
                                            category='business',
                                            language='en')


    # /v2/top-headlines/sources
    sources = newsapi.get_sources()
    
    return sources

## from newsdata.io
def fetch_financial_news_newsdataio():
    url = "https://newsdata.io/api/1/news?apikey=pub_42330810c1d208f46c7a3aa4cada9cccaaeac&language=en "
    response = requests.get(url)
    return response.json()


## from Yahoo finance
def fetch_Yahoo_financial_news_famous_brand():
    # tsla
    url = "https://yahoo-finance127.p.rapidapi.com/news/tsla"

    headers = {
        "X-RapidAPI-Key": "e3ffde7ad0msh33323e10f821f13p15885bjsn25fc84293c2a",
        "X-RapidAPI-Host": "yahoo-finance127.p.rapidapi.com"
    }

    response_tsla = requests.get(url, headers=headers)

    # apple
    url = "https://yahoo-finance127.p.rapidapi.com/news/apple"

    headers = {
        "X-RapidAPI-Key": "e3ffde7ad0msh33323e10f821f13p15885bjsn25fc84293c2a",
        "X-RapidAPI-Host": "yahoo-finance127.p.rapidapi.com"
    }

    response_apple = requests.get(url, headers=headers)
    
    
    # nvdia
    url = "https://yahoo-finance127.p.rapidapi.com/news/nvdia"

    headers = {
        "X-RapidAPI-Key": "e3ffde7ad0msh33323e10f821f13p15885bjsn25fc84293c2a",
        "X-RapidAPI-Host": "yahoo-finance127.p.rapidapi.com"
    }

    response_nvdia = requests.get(url, headers=headers)
    
    # amazon

    url = "https://yahoo-finance127.p.rapidapi.com/news/amazon"

    headers = {
        "X-RapidAPI-Key": "e3ffde7ad0msh33323e10f821f13p15885bjsn25fc84293c2a",
        "X-RapidAPI-Host": "yahoo-finance127.p.rapidapi.com"
    }

    response_amazon = requests.get(url, headers=headers)

    return [response_tsla.json(),response_apple.json(),response_nvdia.json(),response_amazon.json()]


def fetch_financial_news_apple():

	url = "https://real-time-finance-data.p.rapidapi.com/stock-news"

	querystring = {"symbol":"AAPL:NASDAQ","language":"en"}

	headers = {
		"X-RapidAPI-Key": "e3ffde7ad0msh33323e10f821f13p15885bjsn25fc84293c2a",
		"X-RapidAPI-Host": "real-time-finance-data.p.rapidapi.com"
	}

	response = requests.get(url, headers=headers, params=querystring)

	return response.json()



def fetch_financial_news_tsla2():

	url = "https://newsapi.org/v2/everything?q=tesla&from=2024-03-20&sortBy=publishedAt&apiKey=e20960921b7c4bc7ad4fd59ea6537d45"

	response = requests.get(url)

	return response.json()

    
def fetch_news_everything(): 
	url = ('https://newsapi.org/v2/everything?'
		'q=Apple&'
		'from=2024-04-10&'
		'sortBy=popularity&'
		'apiKey=e20960921b7c4bc7ad4fd59ea6537d45')

	response = requests.get(url)
	return response.json()
