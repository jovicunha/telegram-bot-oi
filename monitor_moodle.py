from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import os

# ===== CONFIGURAÇÃO =====
URL = "https://campus.upecde.edu.py:5022/moodle/mod/attendance/view.php?id=325"
USUARIO = "MD30295CDE24"
SENHA = "Parada23"

# ===== TELEGRAM =====
TELEGRAM_TOKEN = "8540217421:AAGdfsY40D15sf7KtCvv7KW4BMW8PTUz9VY"
CHAT_ID = "6433432837"
MENSAGEM = "Sua presença foi registrada, segue comprovante!"

# ===== CONFIGURAR CHROME HEADLESS =====
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
options.add_argument("--ignore-certificate-errors")

# ===== CORREÇÃO: Usando Service =====
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # ===== ABRIR SITE =====
    driver.get(URL)
    time.sleep(8)

    # ===== LOGIN =====
    driver.find_element(By.ID, "username").send_keys(USUARIO)
    driver.find_element(By.ID, "password").send_keys(SENHA)
    driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
    time.sleep(8)

 
    # ===== AJUSTA JANELA PARA PRINT =====
    total_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(1920, total_height)

    # ===== TIRA PRINT =====
    screenshot_path = "comprovante.png"
    driver.save_screenshot(screenshot_path)

    # ===== ENVIA PARA TELEGRAM =====
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    with open(screenshot_path, "rb") as foto:
        requests.post(
            url,
            data={"chat_id": CHAT_ID, "caption": MENSAGEM},
            files={"photo": foto}
        )

    print("Print enviado para o Telegram!")

finally:
    driver.quit()
