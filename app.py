from time import sleep  # Importa la función sleep para pausas
from selenium import webdriver  # Importa Selenium para control del navegador
from selenium.webdriver.common.by import By  # Importa By para localización de elementos
from selenium.webdriver.chrome.options import Options # Importa Options para configurar Chrome
from selenium.webdriver.chrome.service import Service  # Importa Service para manejar el servicio de Chrome
from selenium.webdriver.support.ui import WebDriverWait, Select  # Importa WebDriverWait y Select para manejar esperas explícitas y listas desplegables
from selenium.webdriver.support import expected_conditions as EC  # Importa condiciones esperadas para las esperas
from selenium.common.exceptions import NoSuchElementException  # Importa las excepciones de Selenium

from webdriver_manager.chrome import ChromeDriverManager  # Importa ChromeDriverManager para manejar el driver de Chrome

opts = Options()  # Crea una instancia de opciones de Chrome

# Configuración de user agent:
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")  # Añade un user agent específico
opts.add_argument("--headless") # Añade la opción headless para no abrir la ventana del navegador

# Deshabilitar los logs de la consola de DevTools
opts.add_argument("--log-level=3")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),  # Instala y usa el driver de Chrome
    options=opts  # Aplica las opciones configuradas
)

driver.get('https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp')  # Accede a la URL de SUNAT

sleep(3)  # Espera 3 segundos para asegurar que la página cargue

# Función para buscar por RUC
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
        except NoSuchElementException as e:
            print(f"Error al extraer información de un elemento: {e}")

# Función para buscar por documento
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
    items = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".list-group-item")))
    
    # Extraer y mostrar encabezados y textos utilizando XPath
    for i, item in enumerate(items, start=1):
        try:
            heading = item.find_element(By.CSS_SELECTOR, "h4.list-group-item-heading").text
            text = item.find_element(By.CSS_SELECTOR, "p.list-group-item-text").text
            print(f"Item {i}: Encabezado - {heading}, Texto - {text}")
        except NoSuchElementException:
            print(f"Item {i}: No se encontró el elemento esperado.")

# Función para buscar por nombre o razón social
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
buscar_por_documento('documento nacional de identidad', '46878365')
sleep(10)  # Tiempo para observar los resultados

"""# Ejemplo de uso
buscar_por_ruc('20605431543')
sleep(10)  # Tiempo para observar los resultados

# Ejemplo de uso
buscar_por_nombre_razon_social('TIENDAS POR DEPARTAMENTO RIPLEY S.A.C.')
sleep(10)  # Tiempo para observar los resultados

# Ejemplo de uso
buscar_por_documento('Carnet de Extranjeria', '001077238')
sleep(10)  # Tiempo para observar los resultados
"""
# Cerrar el navegador
driver.quit()


