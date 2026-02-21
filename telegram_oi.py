import os
import requests

# ===== CONFIGURAÇÃO =====
TOKEN = os.getenv("TELEGRAM_TOKEN")     # token do bot no GitHub Secrets
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") # chat_id no GitHub Secrets
MENSAGEM = "Oi do GitHub Actions!"      # mensagem que será enviada

# ===== ENVIO =====
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = {
    "chat_id": CHAT_ID,
    "text": MENSAGEM
}

resposta = requests.post(url, data=data)

if resposta.status_code == 200:
    print("Mensagem enviada com sucesso!")
else:
    print("Erro ao enviar mensagem:", resposta.text)
