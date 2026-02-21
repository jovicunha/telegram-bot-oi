import os
import requests
import re
import subprocess
from datetime import datetime

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
    print("📥 Abrindo página de login...")
    login_page = session.get(URL_LOGIN, verify=False)

    token_match = re.search(r'name="logintoken" value="(.+?)"', login_page.text)
    if not token_match:
        raise Exception("Token de login não encontrado")
    logintoken = token_match.group(1)

    print("🔑 Realizando login...")
    payload = {
        "username": USUARIO,
        "password": SENHA,
        "logintoken": logintoken
    }
    session.post(URL_LOGIN, data=payload, verify=False)

    print("📄 Acessando página de presença...")
    pagina = session.get(URL, verify=False)

    # ===== Gerar nome único para print =====
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_path = f"pagina_{timestamp}.html"
    screenshot_path = f"comprovante_{timestamp}.png"

    # ===== Salvar HTML temporário =====
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(pagina.text)

    print("🖼️ Convertendo HTML em imagem...")
    result = subprocess.run([
        "wkhtmltoimage",
        "--width", "1280",
        html_path,
        screenshot_path
    ], capture_output=True, text=True)

    print("stdout:", result.stdout)
    print("stderr:", result.stderr)

    if not os.path.exists(screenshot_path):
        raise Exception("Erro: arquivo de print não foi criado!")

    print("📩 Enviando print para Telegram...")
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    with open(screenshot_path, "rb") as foto:
        response = requests.post(
            url,
            data={"chat_id": CHAT_ID, "caption": MENSAGEM},
            files={"photo": foto}
        )
    if response.status_code != 200:
        raise Exception(f"Erro ao enviar Telegram: {response.text}")

    print("✅ Print enviado com sucesso!")

except Exception as e:
    print("❌ Erro:", e)
