from selenium import webdriver #Importar el módulo de WebDriver para controlar el navegador
from selenium.webdriver.chrome.service import Service #Importar el módulo de servicio para especificar la ruta del chromedriver
from selenium.webdriver.support.ui import WebDriverWait, Select #Importar WebDriverWait para manejar esperas explícitas
from selenium.webdriver.support import expected_conditions as EC #Importar condiciones esperadas para las esperas
from selenium.webdriver.common.by import By # Importar By para seleccionar elementos por
from selenium.common.exceptions import NoSuchElementException
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

#funcion para buscar por ruc:
def buscar_por_ruc(ruc):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnPorRuc"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "txtRuc"))).send_keys(ruc)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnAceptar"))).click()
    # Esperar a que los elementos de la lista sean visibles y almacenarlos en una lista
    items = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".list-group-item")))
    
    # Recorrer cada elemento y extraer los datos de h4 y p
    for item in items:
        try:
            heading = item.find_element(By.CSS_SELECTOR, "h4.list-group-item-heading").text
            text = item.find_element(By.CSS_SELECTOR, "p.list-group-item-text").text
            print(f"Encabezado: {heading}, Texto: {text}")
        except Exception as e:
            print(f"Error al extraer información de un elemento: {e}")

#funcion para buscar por documento:
def buscar_por_documento(tipo_documento, numero_documento):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnPorDocumento"))).click()
    select = Select(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "cmbTipoDoc"))))

    if tipo_documento.lower() == 'documento nacional de identidad':
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "txtNumeroDocumento"))).send_keys(numero_documento)
    elif tipo_documento.lower() == 'carnet de extranjeria':
        select.select_by_value('4')  # Usando el atributo value para Carnet de Extranjeria
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "txtNumeroDocumento"))).send_keys(numero_documento)
    elif tipo_documento.lower() == 'pasaporte':
        select.select_by_value('7')  # Valor para Pasaporte
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "txtNumeroDocumento"))).send_keys(numero_documento)
    elif tipo_documento.lower() == 'cedula diplomatica de identidad':
        select.select_by_value('A')  # Valor para Cedula Diplomática de Identidad
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "txtNumeroDocumento"))).send_keys(numero_documento)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnAceptar"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.list-group-item.clearfix.aRucs"))).click()
    # Esperar a que los elementos de la lista sean visibles
    items = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".list-group-item"))
    )
    
    # Extraer y mostrar encabezados y textos utilizando XPath
    for i, item in enumerate(items, start=1):
        try:
            heading = item.find_element(By.CSS_SELECTOR, "h4.list-group-item-heading").text
            text = item.find_element(By.CSS_SELECTOR, "p.list-group-item-text").text
            print(f"Item {i}: Encabezado - {heading}, Texto - {text}")
        except NoSuchElementException:
            print(f"Item {i}: No se encontró el elemento esperado.")
#funcion para buscar por nombre o razon social:
def buscar_por_nombre_razon_social(nombre_razon):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnPorRazonSocial"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "txtNombreRazonSocial"))).send_keys(nombre_razon)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnAceptar"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.list-group-item.clearfix.aRucs"))).click()
      # Extracción de datos con XPath
    text_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='list-group-item'][1]/div/div[2]/h4")))
    ruc_text = text_element.text
    print("Número de RUC y Nombre:", ruc_text)

    tipo_contribuyente_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='list-group-item'][2]/div/div[2]/p")))
    tipo_contribuyente_text = tipo_contribuyente_element.text
    print("Tipo Contribuyente:", tipo_contribuyente_text)


# Ejemplo de uso
buscar_por_documento('documento nacional de identidad', '45282085')
time.sleep(10)  # Tiempo para observar los resultados

"""# Ejemplo de uso
buscar_por_ruc('20605431543')
time.sleep(10)  # Tiempo para observar los resultados"""

"""#Ejemplo de uso
buscar_por_nombre_razon_social('TIENDAS POR DEPARTAMENTO RIPLEY S.A.C.')
time.sleep(10)  # Tiempo para observar los resultados"""

"""#Ejemplo de uso
buscar_por_documento('Carnet de Extranjeria', '001077238')
time.sleep(10)  # Tiempo para observar los resultados"""

# Cerrar el navegador
driver.quit()



