import os
import requests
import re

# ===== CONFIGURAÇÃO =====
URL = "https://campus.upecde.edu.py:5022/moodle/mod/attendance/view.php?id=325"
URL_LOGIN = "https://campus.upecde.edu.py:5022/moodle/login/index.php"

USUARIO = os.getenv("MOODLE_USER")
SENHA = os.getenv("MOODLE_PASS")

# ===== TELEGRAM =====
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MENSAGEM = "Sua presença foi registrada, segue comprovante!"

# ⚠️ Ignorar aviso de SSL inseguro
requests.packages.urllib3.disable_warnings()

session = requests.Session()

try:
    # ===== 1) ABRIR LOGIN =====
    login_page = session.get(URL_LOGIN, verify=False)

    token_match = re.search(r'name="logintoken" value="(.+?)"', login_page.text)
    if not token_match:
        raise Exception("Token de login não encontrado")

    logintoken = token_match.group(1)

    # ===== 2) FAZER LOGIN =====
    payload = {
        "username": USUARIO,
        "password": SENHA,
        "logintoken": logintoken
    }

    session.post(URL_LOGIN, data=payload, verify=False)

    # ===== 3) ABRIR PÁGINA DA PRESENÇA =====
    pagina = session.get(URL, verify=False)

    # ===== 4) SALVAR COMPROVANTE =====
    screenshot_path = "comprovante.html"
    with open(screenshot_path, "w", encoding="utf-8") as f:
        f.write(pagina.text)

    # ===== 5) ENVIAR PARA TELEGRAM =====
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"

    with open(screenshot_path, "rb") as arquivo:
        requests.post(
            url,
            data={"chat_id": CHAT_ID, "caption": MENSAGEM},
            files={"document": arquivo}
        )

    print("Comprovante enviado!")

except Exception as e:
    print("Erro:", e)
