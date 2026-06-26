# Telegram News Bot

Um bot para Telegram que coleta, resume e envia as principais notícias do dia automaticamente para os usuários inscritos.

O projeto consome feeds RSS do Google News, extrai o texto completo das matérias contornando links criptografados e utiliza a API do Groq para criar resumos concisos. O sistema foi desenhado para rodar 24/7 de forma assíncrona, disparando um boletim diário programado para a base de usuários.

## Deploy e Infraestrutura

O projeto está em produção, com o deploy realizado em um servidor Linux na plataforma **Alwaysdata**. A arquitetura da infraestrutura envolve:
- Conexão e transferência de arquivos via protocolos seguros (SSH/SFTP).
- Configuração de ambiente virtual Python (`venv`) remoto.
- Gerenciamento de processos em background (Services) para manter a aplicação rodando 24/7.
- Armazenamento persistente no disco do servidor para o banco de dados.

## Funcionalidades

- **Gerenciamento de Inscritos:** Cadastro simples via comando `/start` e remoção imediata via comando `/stop` (respeitando o controle de dados do usuário).
- **Web Scraping:** Leitura automatizada de RSS do Google e extração inteligente do corpo das matérias originais.
- **Resumos com IA:** Integração com LLM (Groq) para sintetizar grandes volumes de texto em resumos diretos.
- **Disparo Programado:** Envio do boletim diário em lote utilizando fila de tarefas (Job Queue) assíncrona.
- **Persistência de Dados:** Banco de dados relacional leve (SQLite) para gerenciar as permissões e IDs dos usuários ativos.

## Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Bot Framework:** `python-telegram-bot`
- **Inteligência Artificial:** llama-3.1-8b-instant (via API do Groq)
- **Web Scraping:** `newspaper4k` e `feedparser`
- **Banco de Dados:** SQLite
- **Hospedagem:** Alwaysdata (Servidor Linux)

## Como rodar o projeto localmente

### Pré-requisitos
- Python 3.8+ instalado.
- Token de um bot no Telegram (obtido via BotFather).
- Chave de API do Groq.

### Instalação

1. Clone o repositório:

    git clone https://github.com/Farae1/News_telegram.git
    cd News_telegram

2. Crie e ative o ambiente virtual:

    python3 -m venv .venv
    source .venv/bin/activate

3. Instale as dependências:

    pip install -r requirements.txt

4. Configure as variáveis de ambiente (crie um arquivo `.env` na raiz do projeto):

    TOKEN_TELEGRAM=seu_token_do_telegram_aqui
    GROQ_API_KEY=sua_chave_do_groq_aqui

5. Inicie o banco de dados e o bot:

    python bot.py
