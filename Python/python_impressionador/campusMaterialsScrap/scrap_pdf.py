from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from time import sleep
import base64


# Inicializa o serviço e o navegador
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)
navegador.get('https://www.campusplastics.com')
sleep(3)

# Clica no botão para mostrar a lista de datasheets
navegador.find_element(By.ID, 'searchmatlist').click()

# Espera até que todos os elementos de datasheet estejam visíveis
WebDriverWait(navegador, 10).until(
    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a[alt^="CAMPUS Datasheet for"]'))
)

# Coleta todos os links de datasheet
datasheet_links = navegador.find_elements(By.CSS_SELECTOR, 'a[alt^="CAMPUS Datasheet for"]')

urls = []

for link in datasheet_links:
    url =link.get_attribute('href')
    urls.append(url)

# Itera sobre os links
for url in urls:


    # Entra no datasheet
    navegador.get(url)
    sleep(6)
    # Pega o conteúdo do datasheet e transforma em texto
    datasheet = navegador.find_element(By.ID, 'datasheetbody').text
    # Formata o nome do arquivo
    caracteres_invalidos = ['/', '\\', '?', '%', '*', ':', '|', '"', '<', '>', '.']
    primeira_linha = datasheet.strip().split('\n')[0]
    nome_arquivo = ''.join(c for c in primeira_linha if c not in caracteres_invalidos)
    # PDF
    datasheet_pdf = navegador.execute_cdp_cmd('Page.printToPDF',{
        "printBackground": True
    } )

    with open(nome_arquivo + '.pdf', "wb") as f:
        f.write(base64.b64decode(datasheet_pdf['data']))