from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
import re
from urllib.parse import urljoin 

# Configurando o WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Executar em segundo plano
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

def converter_data(data_str):
    meses = {
        "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04", "maio": "05",
        "junho": "06", "julho": "07", "agosto": "08", "setembro": "09", "outubro": "10",
        "novembro": "11", "dezembro": "12"
    }
    match = re.match(r"(\d{1,2}) de (\w+) de (\d{4})", data_str)
    if match:
        dia = match.group(1).zfill(2)  # Captura o dia e adiciona zero à esquerda se necessário
        mes = match.group(2)  # Captura o mês
        ano = match.group(3)  # Captura o ano
        return f"{ano}-{meses[mes]}-{dia} 14:00:00"
    else:
        raise ValueError("Formato de data inválido!")

base_url = "https://alfamaweb.com.br"

# URL do blog
url = base_url + "/nosso-blog/"
driver.get(url)

# Clicar 3 vezes no botão "Carregar Mais"
for _ in range(3):
    try:
        botao = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.paginacao.btn-ver-mais")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", botao)
        time.sleep(3)  # Aguarda carregamento dos novos posts
    except Exception as e:
        print(f"Erro ao clicar no botão: {e}")
        break

# Extraindo o HTML após carregamento
soup = BeautifulSoup(driver.page_source, "html.parser")

# Encontrar todos os posts
posts = soup.find_all("div", class_="post")

geral = []

for post in posts:
    # Extrair link do post
    link_elem = post.find("a", href=True)
    link = link_elem["href"] if link_elem else None
    
    if link and link.startswith("/"):
        link = urljoin(base_url, link)

    # Extrair título do post
    titulo_elem = post.find("p")
    titulo = titulo_elem.text.strip() if titulo_elem else "Sem título"

    # Extrair categoria
    categoria_elem = post.find("small")
    categoria = categoria_elem.text.strip() if categoria_elem else "Sem categoria"

    # Extrair imagem do post (background)
    bg_elem = post.find("div", class_="bg-post")
    imagem = None
    if bg_elem and "background" in bg_elem.get("style", ""):
        match = re.search(r"url\(['\"]?(.*?)['\"]?\)", bg_elem["style"])
        if match:
            imagem = match.group(1)

    # Criando dicionário do post
    item = {
        "titulo": titulo,
        "categoria": categoria,
        "data": None,
        "imagem": imagem,
        "conteudo": None,
        "link": link
    }
    
    if link:
        driver.get(link)
        time.sleep(2)  # Aguarda o carregamento da página do post

        # Encontrar o conteúdo do post na div .leitura
        post_soup = BeautifulSoup(driver.page_source, "html.parser")
        conteudo_elem = post_soup.find("div", class_="leitura")
        conteudo = conteudo_elem.text.strip() if conteudo_elem else "Conteúdo não encontrado"
        
        data_texto_tag = post_soup.find('p', class_='data-post d-inline-block')
        print(data_texto_tag)
        
        if data_texto_tag:
            data_texto = data_texto_tag.text.strip()
            data = converter_data(data_texto)  # Passar a string para a função
            print(data)
        else:
            data = "Data não encontrada"
        
        # Atualizar o item com o conteúdo extraído
        item["conteudo"] = conteudo
        item["data"] = data

    print(item)
    geral.append(item)

# Salvando os dados em JSON
with open("C:/Users/igorj/OneDrive/Documentos/Code/Automações/AlfamaDecoded.json", "w", encoding="utf-8") as f:
    json.dump(geral, f, ensure_ascii=False, indent=4)

print("Dados salvos com sucesso!")

# Fechar navegador
driver.quit()
