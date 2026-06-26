import os
import sqlite3
import datetime
import asyncio
from zoneinfo import ZoneInfo
from main import gerar_boletim
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Carrega as variáveis do arquivo .env
load_dotenv()


def iniciar_banco():
    conexao = sqlite3.connect("inscritos.db")
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER UNIQUE
        )
    ''')

    conexao.commit()
    conexao.close()


def remover_inscrito(user_id):
    conexao = sqlite3.connect("inscritos.db")
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id_usuario = ?", (user_id,))

    conexao.commit()
    conexao.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id_cliente = update.message.chat_id

    conexao = sqlite3.connect("inscritos.db")
    cursor = conexao.cursor()

    cursor.execute("INSERT OR IGNORE INTO usuarios (id_usuario) VALUES (?)", (id_cliente,))

    conexao.commit()
    conexao.close()

    await update.message.reply_text("Inscrição confirmada! Você receberá nosso boletim de notícias aqui. Se não quiser mais, só mandar um /stop")


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    remover_inscrito(user_id)

    await update.message.reply_text(
        "Sua inscrição foi cancelada com sucesso. "
        "Você não receberá mais os resumos diários. "
        "Se quiser voltar, é só mandar um /start a qualquer momento!"
    )

def fatiar_mensagem(texto, limite=4000):
    pedacos = []
    pedaco_atual = ""

    noticias = texto.split('\n\n')

    for noticia in noticias:
        if len(pedaco_atual) + len(noticia) + 2 <= limite:
            pedaco_atual += noticia + "\n\n"
        else:
            if pedaco_atual:
                pedacos.append(pedaco_atual)
            pedaco_atual = noticia + "\n\n"

    if pedaco_atual:
        pedacos.append(pedaco_atual)

    return pedacos


async def disparar_noticias_da_noite(context: ContextTypes.DEFAULT_TYPE):
    texto_gigante = await asyncio.to_thread(gerar_boletim)
    lista_de_baloes = fatiar_mensagem(texto_gigante)

    conexao = sqlite3.connect("inscritos.db")
    cursor = conexao.cursor()

    cursor.execute('SELECT id_usuario FROM usuarios')
    IDs = cursor.fetchall()

    for linha in IDs:
        ID_puro = linha[0]

        for balao in lista_de_baloes:
            await context.bot.send_message(chat_id=ID_puro, text=balao, parse_mode='Markdown')
            await asyncio.sleep(1)

    conexao.close()
if __name__ == '__main__':
    iniciar_banco()

    token_telegram = os.getenv("TOKEN_TELEGRAM")
    app = ApplicationBuilder().token(token_telegram).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))

    # ---- CONFIGURAÇÃO DO RELÓGIO ----
    horario_alvo = datetime.time(hour=20, minute=0, second=0, tzinfo=ZoneInfo("America/Sao_Paulo"))

    # Agendamento Dispara todo dia às 20h:
    app.job_queue.run_daily(disparar_noticias_da_noite, time=horario_alvo)


    print("Bot online e aguardando...")
    app.run_polling()