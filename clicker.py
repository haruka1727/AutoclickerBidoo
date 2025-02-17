import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configura il driver per Chromium
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Rimuovi il commento se vuoi eseguire in background
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)  # Assicurati che chromedriver sia nel PATH

def apri_e_clicca(url, button_selector, email_selector, password_selector, login_button_selector, credenziali):
    try:
        driver.get(url)
        print("🌍 Apertura URL:", url)
        
        # Memorizza la finestra principale
        main_window = driver.current_window_handle

        # Trova e clicca il pulsante
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector))
        )
        button.click()
        print("✅ Pulsante cliccato con successo!")

        # Attendi e passa alla nuova finestra
        WebDriverWait(driver, 10).until(
            lambda driver: len(driver.window_handles) > 1
        )
        for window_handle in driver.window_handles:
            if window_handle != main_window:
                driver.switch_to.window(window_handle)
                print("✅ Passato alla nuova finestra:", driver.current_url)
                break

        # Inserisci email e password
        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, email_selector))
        )
        password_field = driver.find_element(By.CSS_SELECTOR, password_selector)

        email_field.send_keys(credenziali["email"])
        password_field.send_keys(credenziali["password"])
        print(f"🔑 Inserita email: {credenziali['email']}")

        # Clicca sul pulsante di login
        login_button = driver.find_element(By.CSS_SELECTOR, login_button_selector)
        login_button.click()
        print("✅ Login effettuato!")

        # Attendi per verificare il login
        WebDriverWait(driver, 10).until(
            EC.url_changes(driver.current_url)
        )
        print("✅ Pagina aggiornata dopo il login!")

    except Exception as e:
        print("❌ Errore:", e)

def esegui_login_multiple(account_list, url, button_selector, email_selector, password_selector, login_button_selector):
    for credenziali in account_list:
        apri_e_clicca(url, button_selector, email_selector, password_selector, login_button_selector, credenziali)
        print("🔄 Passo al prossimo account...\n")

# Leggi le credenziali dal file JSON
with open("credenziali.json", "r") as file:
    account_list = json.load(file)

# Selettori dei campi di login (modifica in base al sito)
url = "https://tuttoapoco.com/puntate/#"
button_selector = "#auto0"  # Usa l'ID per maggiore precisione
email_selector = "#field_email"  # Modifica con il selettore corretto per email
password_selector = "#password"  # Selettore per il campo password
login_button_selector = ".btlogin"  # Selettore per il pulsante "ENTRA"

# Esegui l'autoclicker per tutti gli account
esegui_login_multiple(account_list, url, button_selector, email_selector, password_selector, login_button_selector)

# Chiudi il browser alla fine
driver.quit()
