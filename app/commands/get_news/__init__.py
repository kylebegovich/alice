import sys, os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants
import urllib2, json

NEWS_API_URL = "https://newsapi.org/v1/articles?source=the-new-york-times&sortBy=top&apiKey="

key_file = open("api_key.txt", 'r')
NEWS_API_KEY = key_file.read()
key_file.close()

NEWS_API_URL += NEWS_API_KEY

NUM_ARTICLES = 5

def get_news(query, **kwargs):
    jstr = urllib2.urlopen(NEWS_API_URL).read()
    ts = json.loads( jstr )
    for i in range(NUM_ARTICLES):
        headline = ( str(i+1) +  ". " + ts['articles'][i]['title'] )
        headline = ''.join([i if ord(i) < 128 else ' ' for i in headline])
        print headline
        os.system(constants.DISPLAY_NOTIFICATION % (headline,))

TRIGGER_MODEL = "GET_NEWS.model"
FUNC = get_news

