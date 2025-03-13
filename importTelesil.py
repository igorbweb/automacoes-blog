import requests
from bs4 import BeautifulSoup
import json
import re

def converter_data(data_str):
    data = data_str.split('/')
    data.reverse()
    data = ', '.join(data)
    resultado = data.replace(', ', '-')
    if resultado:
        
        return f"{resultado} 14:00:00"
    else:
        raise ValueError("Formato de data inválido!")

url_base = 'https://www.telesilengenharia.com.br/blogs/?page={}'
num_paginas = 13
geral = []
site_base = 'https://www.telesilengenharia.com.br'

for i in range(1, num_paginas + 1):
    url = url_base.format(i)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ajuste conforme a estrutura do site
        posts = soup.find_all('a', class_='blog-content__card')  

        for post in posts:
            titulo_elem = post.find('h1')
            imagem_elem = post.find('figure')
            link_elem = post['href']
            data_elem = post.find('span')

            titulo = titulo_elem.text.strip() if titulo_elem else 'Sem título'
            imagem = imagem_elem.find('img')['src'] if imagem_elem and imagem_elem.find('img') else 'Sem imagem'
            # link_pagina_interna = link_elem['href'] if link_elem else None
            data_texto = data_elem.text.strip() if data_elem else None
            data = converter_data(data_texto)

            conteudo = 'Sem conteúdo' # Valor padrão caso falhe a captura

            if link_elem:
                if not link_elem.startswith("http"):
                    link_elem = site_base + link_elem  # Garante que a URL seja absoluta

                response_interna = requests.get(link_elem)

                if response_interna.status_code == 200:
                    soup_interna = BeautifulSoup(response_interna.text, 'html.parser')

                    # Busca o conteúdo na página interna corretamente
                    conteudo_elem = soup_interna.find('div', class_='socio-info')

                    if conteudo_elem:
                        conteudo = conteudo_elem.decode_contents()  # Mantém a estrutura HTML
                    else:
                        print(f"Div não encontrada na {link_elem}")
                else:
                    print(f"Erro ao acessar {link_elem}, status code: {response_interna.status_code}")

            item = {
                'titulo': titulo,
                'imagem': site_base+imagem,
                'data': data,
                'link': link_elem,
                'conteudo': conteudo,
            }

            print(item)
            geral.append(item)
    else:
        print(f'Erro ao acessar {url}, status code: {response.status_code}')


# # Salvando os dados coletados em um arquivo JSON
with open('C:/Users/igorf/Documents/Code/Telesil.json', 'w', encoding='utf-8') as f:
    json.dump(geral, f, ensure_ascii=False, indent=4)

print("Dados salvos com sucesso!")
