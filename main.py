import feedparser
import os
import time
from dotenv import load_dotenv
from newspaper import Article, Config
from googlenewsdecoder import new_decoderv1
from groq import Groq


def gerar_boletim():
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=groq_api_key)

    user_choose = "tecnologia"
    list_articles = []
    boletim_final = " *Boletim de Notícias*\n\n"

    config_navegador = Config()
    config_navegador.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

    # Busca das 20 primeiras noticias no RRS Feed do Google News e extração do titulo, link e texto em uma lista
    rss_parsing = feedparser.parse("https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419")
    list_news = rss_parsing.entries[:20]

    for entry in list_news:
        try:
            link = new_decoderv1(entry["link"], interval=5)
            article = Article(link["decoded_url"], config=config_navegador)
            article.download()
            article.parse()

            if article.text.strip():
                list_articles.append({"link": link["decoded_url"], "title": entry["title"], "text": article.text})
        except Exception:
            continue

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

        try:
            awnser = client.chat.completions.create(
                messages=messages_package,
                model="llama-3.1-8b-instant"
            )
            resume_awnser = awnser.choices[0].message.content
            article["resume"] = resume_awnser

            boletim_final += f"🔹 *{article['title']}*\n{resume_awnser}\n🔗 {article['link']}\n\n"
        except Exception:
            continue

        time.sleep(5)

    return boletim_final