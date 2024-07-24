from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

#Opciones de navegación:
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

#Ruta del driver
driver_path = r'C:\SeleniumDrivers\chromedriver.exe'  
service = Service(driver_path)

#Inicializar el navegador
driver = webdriver.Chrome(service=service, options=options)

#Navegar a la URL
driver.get('https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp')


#rellenar en el campo para el ruc:
WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#txtRuc'))
    ).send_keys('20612534242')

#hacer click:
WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn btn-primary'.replace(' ', '.')))
    ).click()

time.sleep(10)
driver.quit()
