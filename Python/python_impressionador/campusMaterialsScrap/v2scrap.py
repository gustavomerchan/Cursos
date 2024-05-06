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

def coletar_urls():
    # Clica no botão para mostrar a lista de datasheets
    navegador.find_element(By.ID, 'searchmatlist').click()

    # Espera até que todos os elementos de datasheet estejam visíveis
    WebDriverWait(navegador, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a[alt^="CAMPUS Datasheet for"]'))
    )

    # Coleta todos os links de datasheet
    datasheet_links = navegador.find_elements(By.CSS_SELECTOR, 'a[alt^="CAMPUS Datasheet for"]')
    urls = [link.get_attribute('href') for link in datasheet_links]
    return urls

indice_inicio = 45

# Processa todas as páginas
while True:
    urls = coletar_urls()

    # Itera sobre os links
    for url in urls[indice_inicio:]:
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
        datasheet_pdf = navegador.execute_cdp_cmd('Page.printToPDF', {
            "printBackground": True
        })

        with open(nome_arquivo + '.pdf', "wb") as f:
            f.write(base64.b64decode(datasheet_pdf['data']))

    # Verifica se existe um botão de 'próxima página' e navega para ele
    try:
        proxima_pagina = navegador.find_element(By.CLASS_NAME, 'icons icons-resultset-next')  # Ou By.CSS_SELECTOR, se usar um seletor CSS
        proxima_pagina.click()
        sleep(3)  # Espera a página carregar
    except:
        print("Não há mais páginas para processar.")
        break

# Fechar o navegador
navegador.quit()
