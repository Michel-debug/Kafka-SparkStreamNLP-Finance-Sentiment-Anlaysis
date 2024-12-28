from kafka import KafkaProducer
import json
import re
import api_News

# Clean data rules
pattern = re.compile(r'^[a-zA-Z0-9\s.,!?\'"()-]*$')

# kafka's configuration
kafka_server = 'localhost:9093'
topic_name = 'finance-news'

# create Kafka producer，message code as UTF-8
producer = KafkaProducer(bootstrap_servers=kafka_server,
                         value_serializer=lambda m: json.dumps(m).encode('utf-8'))

# send news to kafka fonction
def send_news_to_kafka(headline):
    try:
        future = producer.send(topic_name, value=headline)
        result = future.get(timeout=10)
        print(f"Sent and acknowledged: {headline} at offset {result.offset}")
    except Exception as e:
        print(f"Failed to send headline to Kafka: {headline}, Error: {e}")
    

# excute the fetch and send news
news_apis = [
    (api_News.fetch_bbc_news, "BBC"),
    (api_News.fetch_financial_news_seekingalpha, "SeekingAlpha"),
    (api_News.fetch_financial_news_newsdataio, "NewsdataIO"),
    (api_News.fetch_Yahoo_financial_news_famous_brand, "Yahoo"),
    (api_News.fetch_financial_news_apple, "Apple"),
    (api_News.fetch_financial_news_tsla2, "Tesla"),
    (api_News.fetch_news_everything, "Everything")
]

def fetch_and_send_news(api_method, api_name):
    try:
        sources_news = api_method()
        if api_name=="Yahoo":
            for source in sources_news:
                for i in source.keys():
                # try to send the news to kafka, ifnot exception
                    send_news_to_kafka(source[i]['title'])

        elif api_name=="Apple" and sources_news['status'] == 'ok':
            for source in sources_news['data']['news'] :
                send_news_to_kafka(source['article_title'])
                
        elif api_name=="Tesla" and sources_news['status'] == 'ok':
            for source in sources_news['articles']:
                if(pattern.match(source['title'])):
                    send_news_to_kafka(source['title'])
                    
        elif api_name=="Everything" and sources_news['status'] == 'ok':
            for source in sources_news['articles']:
                if pattern.match(source['title']):
                    send_news_to_kafka(source['title'])
                    
        elif api_name=="BBC" and sources_news['status'] == 'ok':
            for source in sources_news['sources']:
                if pattern.match(source['description']):
                    send_news_to_kafka(source['description'])

        elif api_name=="SeekingAlpha" and 'data' in sources_news:
            for source in sources_news['data']:
                if source['type'] == 'news':
                    send_news_to_kafka(source['attributes']['title'])

        elif api_name=="NewsdataIO" and sources_news['status'] == 'success':
            for source in sources_news['results']:
                send_news_to_kafka(source['title'])
           
    except Exception as e:
        print(f"Error fetching or sending data from {api_name}: {e}, maybe API limit reached, or update the API key, or json structure changed")



for api_method, api_name in news_apis:
    print(f"Fetching news from {api_name}")
    fetch_and_send_news(api_method, api_name)

print("All headlines sent!")