from newspaper import Article
from googlenewsdecoder import new_decoderv1
import feedparser
user_choose= "tecnologia"
list_articles = []
rss_parsing = feedparser.parse(f"https://news.google.com/rss/search?q={user_choose}&hl=pt-BR&gl=BR&ceid=BR:pt-419")
list_news = rss_parsing.entries[:10]
for entry in list_news:
    link = new_decoderv1(entry["link"], interval=5)
    article = Article(link["decoded_url"])
    article.download()
    article.parse()
    list_articles.append({"link" : link["decoded_url"], "title" : entry["title"],"text" : article.text})
print(list_articles)
