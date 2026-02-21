import os
import requests
import re
import subprocess

# ===== CONFIGURAÇÃO =====
URL = "https://campus.upecde.edu.py:5022/moodle/mod/attendance/view.php?id=325"
URL_LOGIN = "https://campus.upecde.edu.py:5022/moodle/login/index.php"

USUARIO = os.getenv("MOODLE_USER")
SENHA = os.getenv("MOODLE_PASS")

# ===== TELEGRAM =====
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MENSAGEM = "Sua presença foi registrada, segue comprovante!"

requests.packages.urllib3.disable_warnings()

session = requests.Session()

try:
    # ===== 1) LOGIN =====
    login_page = session.get(URL_LOGIN, verify=False)

    token_match = re.search(r'name="logintoken" value="(.+?)"', login_page.text)
    if not token_match:
        raise Exception("Token de login não encontrado")

    logintoken = token_match.group(1)

    payload = {
        "username": USUARIO,
        "password": SENHA,
        "logintoken": logintoken
    }

    session.post(URL_LOGIN, data=payload, verify=False)

    # ===== 2) ABRIR PRESENÇA =====
    pagina = session.get(URL, verify=False)

    # ===== 3) SALVAR HTML TEMPORÁRIO =====
    html_path = "pagina.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(pagina.text)

    # ===== 4) CONVERTER PARA IMAGEM =====
    screenshot_path = "comprovante.png"

    subprocess.run([
        "wkhtmltoimage",
        "--width", "1280",
        html_path,
        screenshot_path
    ])

    # ===== 5) ENVIAR FOTO PARA TELEGRAM =====
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"

    with open(screenshot_path, "rb") as foto:
        requests.post(
            url,
            data={"chat_id": CHAT_ID, "caption": MENSAGEM},
            files={"photo": foto}
        )

    print("Print enviado!")

except Exception as e:
    print("Erro:", e)
