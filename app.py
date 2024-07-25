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

#list = []

#def tipo():

#funcion para buscar por ruc:
def buscar_por_ruc(ruc):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnPorRuc"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "txtRuc"))).send_keys(ruc)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnAceptar"))).click()

#funcion para buscar por documento:
def buscar_por_documento(tipo_documento, numero_documento):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnPorDocumento"))).click()
    if tipo_documento.lower() == 'documento nacional de identidad':
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "txtNumeroDocumento"))).send_keys(numero_documento)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnAceptar"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.list-group-item clearfix aRucs".replace(" ", ".")))).click()
    
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "cmbTipoDoc"))).click()
    



#funcion para buscar por nombre o razon social:
def buscar_por_nombre_razon_social(nombre_razon):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnPorRazonSocial"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "txtNombreRazonSocial"))).send_keys(nombre_razon)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnAceptar"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.list-group-item.clearfix.aRucs"))).click()


"""# Ejemplo de uso
buscar_por_ruc('20337564373')
time.sleep(10)  # Tiempo para observar los resultados"""

"""#Ejemplo de uso
buscar_por_nombre_razon_social('TIENDAS POR DEPARTAMENTO RIPLEY S.A.C.')
time.sleep(10)  # Tiempo para observar los resultados"""

#Ejemplo de uso
buscar_por_documento('Documento Nacional de Identidad', '46878365')
time.sleep(10)  # Tiempo para observar los resultados

# Cerrar el navegador
driver.quit()



