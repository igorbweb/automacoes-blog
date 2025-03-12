import requests
from bs4 import BeautifulSoup
import json, codecs
from datetime import datetime
import re

# Função para converter data no formato desejado
def converter_data(data_str):
    meses = {
        "Jan": "01", "Fev": "02", "Mar": "03", "Abr": "04", "Mai": "05",
        "Jun": "06", "Jul": "07", "Ago": "08", "Set": "09", "Out": "10",
        "Nov": "11", "Dez": "12"
    }
    partes = data_str.split(' ')
    dia = partes[0]
    mes = partes[2].replace(",", "")
    ano = partes[4][:4]
    return f"{ano}-{meses[mes]}-{dia} 14:00:00"

# URL base e configuração da paginação
url_base = 'https://www.primasaengenharia.com.br/blog/{}/pages'
numPag = 36
geral = []
site_base = 'https://www.primasaengenharia.com.br'  # URL base do site

# Loop para iterar sobre cada página de listagem
for page in range(1, numPag + 1):
    url = url_base.format(page)
    general = requests.get(url)

    if general.status_code == 200:
        so = BeautifulSoup(general.content, 'html.parser')
        
        # Encontra todos os posts na página atual
        box_noticias = so.find_all('div', class_='boxnoticias')
        if not box_noticias:
            break  # Sai do loop se não encontrar mais posts

        for box in box_noticias:
            post_info = {'titulo': '', 'imagem': '', 'data': '', 'texto': ''}
            
            # Extrair o título do <p class="alt-minima">
            titulo_elemento = box.find('p', class_='alt-minima')
            if titulo_elemento:
                titulo = titulo_elemento.get_text(strip=True)
                post_info['titulo'] = titulo
            else:
                post_info['titulo'] = "Título não encontrado"
            
            # Obter URL do post interno e garantir que é uma URL completa
            link = box.find('a', href=True)
            if link:
                internaUrl = site_base + link['href']  # Concatenando com a URL base
                response = requests.get(internaUrl)

                if response.status_code == 200:
                    # Coleta dos dados na página interna
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extrai imagem do style background da div imgNoticias e remove parâmetros extras
                    img_div = box.find('div', class_='imgNoticias')
                    if img_div and 'style' in img_div.attrs:
                        style = img_div['style']
                        img_url_match = re.search(r'url\((.*?)\)', style)
                        if img_url_match:
                            img_url = img_url_match.group(1).strip('"\'')
                            # Remover parâmetros de largura, altura e qualidade da URL
                            img_url = re.sub(r'(&largura=\d+&altura=\d+&qualidade=\d+)', '', img_url)
                            post_info['imagem'] = img_url
                        else:
                            post_info['imagem'] = "Imagem não encontrada"
                    
                    # Extrai data da div infoNoticia na página de listagem
                    info_noticia = box.find('div', class_='infoNoticia')
                    if info_noticia:
                        data_texto = info_noticia.get_text(strip=True)
                        post_info['data'] = converter_data(data_texto)

                    # Extrai conteúdo HTML da div conteudo_html
                    texto_div = soup.find('div', class_='conteudo_html')
                    post_info['texto'] = texto_div.decode_contents() if texto_div else "Texto não encontrado"

                    # Adiciona informações do post na lista geral
                    geral.append(post_info)
                else:
                    print(f"Erro ao acessar {internaUrl}")
    else:
        print(f"Erro ao acessar {url}")

# Salvando os dados coletados em um arquivo JSON
with open('C:/Users/Alfamaníaco/Documents/Imports/PrimasaDecoded.json', 'w', encoding='utf-8') as f:
    json.dump(geral, f, ensure_ascii=False, indent=4)

print("Dados salvos com sucesso!")
