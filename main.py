import feedparser
import os
import time
from dotenv import load_dotenv
from newspaper import Article
from googlenewsdecoder import new_decoderv1
from groq import Groq

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

user_choose= "tecnologia"
list_articles = []

# Busca das 20 primeiras noticias no RRS Feed do Google News e extração do titulo, link e texto em uma lista
rss_parsing = feedparser.parse("https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419")
list_news = rss_parsing.entries[:20]
for entry in list_news:
    link = new_decoderv1(entry["link"], interval=5)
    article = Article(link["decoded_url"])
    article.download()
    article.parse()
    list_articles.append({"link" : link["decoded_url"], "title" : entry["title"],"text" : article.text})
print(list_articles)
# Conexão com Groq para o boletim diario de noticias
for article in list_articles:
    messages_package = [
        {"role": "system", "content": """Você é um jornalista experiente, direto e objetivo. Sua missão é ler o texto bruto extraído de um site e descobrir qual é a notícia principal, resumindo-a em exatamente um parágrafo curto em português do Brasil.
        Regras estritas:
        Ignore completamente links soltos, propagandas, menus de navegação ou chamadas para outras matérias (como 'leia também' ou links de redes sociais).
        Foque 100% no tema central do texto.
        Não use saudações, introduções ou frases como 'Aqui está o resumo'. Devolva APENAS o texto do resumo pronto para ser publicado"""},

        {"role": "user", "content": article["text"]}
    ]
    awnser = client.chat.completions.create(
        messages=messages_package,
        model="llama3-8b-8192"
    )
    resume_awnser = awnser.choices[0].message.content
    article["resume"] = resume_awnser
    print(article["resume"])
    time.sleep(5)