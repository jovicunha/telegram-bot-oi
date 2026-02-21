import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

# ===== CONFIGURAÇÃO =====
URL = "https://campus.upecde.edu.py:5022/moodle/mod/attendance/view.php?id=325"
USUARIO = os.getenv("MOODLE_USER")
SENHA = os.getenv("MOODLE_PASS")

# ===== TELEGRAM =====
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8540217421:AAGdfsY40D15sf7KtCvv7KW4BMW8PTUz9VY")
CHAT_ID = os.getenv("CHAT_ID", "6433432837")
MENSAGEM = "Sua presença foi registrada, segue comprovante!"

# ===== CONFIGURAR CHROME HEADLESS =====
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# ===== INIT WEBDRIVER =====
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)

try:
    # ===== ABRIR SITE =====
    driver.get(URL)

    # ===== LOGIN =====
    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(USUARIO)
    wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(SENHA)
    driver.find_element(By.ID, "password").send_keys(Keys.RETURN)

    # ===== ESPERA PÁGINA CARREGAR =====
    time.sleep(5)

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
