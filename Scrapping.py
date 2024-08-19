import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Configura el servicio del driver de Selenium
service = Service(executable_path=r"C:\Scrapping\chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Abre LinkedIn e inicia sesión
driver.get('https://www.linkedin.com/login/es?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

# Usa WebDriverWait para esperar a que los elementos estén presentes
wait = WebDriverWait(driver, 10)

try:
    # Encuentra los campos de inicio de sesión
    username = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='username']")))
    password = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='password']")))
    login_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@type='submit']")))

    # Introduce las credenciales y haz clic en el botón de inicio de sesión
    username.send_keys("MAIL")
    password.send_keys("PASS")
    login_button.click()

    sleep(5)  # Ajusta según tu conexión

    # Accede al perfil de LinkedIn
    profile_url = "https://www.linkedin.com/in/anibal-sotelo-989ba726/"
    driver.get(profile_url)

    # Extrae el nombre del perfil
    name = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(@class, 'text-heading-xlarge')]"))
    ).text
    print("Profile name extracted:", name)

    try:
        # Código para extraer experiencias laborales
        driver.execute_script("window.scrollBy(0, 1200)")
        sleep(5)

        experience_elements = driver.find_elements(
            By.XPATH, "//section[contains(@id, 'experience-section')]//ul//li")
        titles = [element.text for element in experience_elements]
        print("Experience titles extracted:", titles)

    except Exception as e:
        print("An error occurred while extracting experience titles:", e)

    # Abre o crea el archivo CSV y escribe la información
    with open("cvs_linkedin.csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nombre', 'puesto_1', 'empresa_1', 'tiempo_empresa_1',
                         'puesto_2', 'empresa_2', 'tiempo_empresa_2',
                         'universidad_1', 'carrera_1', 'universidad_2', 'carrera_2'])
        # Añade datos extraídos en el CSV
        writer.writerow([name] + titles[:2] + [''] * (10 - len(titles)))

finally:
    driver.quit()
