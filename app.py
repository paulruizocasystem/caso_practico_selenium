from selenium import webdriver #Importar el módulo de WebDriver para controlar el navegador
from selenium.webdriver.chrome.service import Service #Importar el módulo de servicio para especificar la ruta del chromedriver
from selenium.webdriver.support.ui import WebDriverWait #Importar WebDriverWait para manejar esperas explícitas
from selenium.webdriver.support import expected_conditions as EC #Importar condiciones esperadas para las esperas
from selenium.webdriver.common.by import By # Importar By para seleccionar elementos por
import time #Importar time para usar sleep y pausar la ejecución
import pandas as pd #Importar pandas, útil para manipular datos

#configuración de opciones para el navegador
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized') #Maximizar la ventana del navegador
options.add_argument('--disable-extensions') #Deshabilitar extensiones

#la ruta del driver
driver_path = r'C:\SeleniumDrivers\chromedriver.exe'  
service = Service(driver_path)

#Inicializa el navegador con las opciones configuradas
driver = webdriver.Chrome(service=service, options=options)

#Acceder a la URL específica
driver.get('https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp')

#Esperar hasta que el campo de RUC sea clicable y enviar el RUC
WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#txtRuc'))
).send_keys('20612534242')

# Esperar hasta que el botón de consulta sea clicable y hacer clic
WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-primary'))
).click()

# Pausar la ejecución para observar los resultados
time.sleep(100)

#Cerrar el navegador
driver.quit()
