import requests
from bs4 import BeautifulSoup
import json
import re

def converter_data(data_str):
    meses = {
        "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04", "maio": "05",
        "junho": "06", "julho": "07", "agosto": "08", "setembro": "09", "outubro": "10",
        "novembro": "11", "dezembro": "12"
    }
    match = re.match(r"(\d{1,2}) de (\w+) de (\d{4})", data_str.lower())
    if match:
        dia = match.group(1).zfill(2)  # Captura o dia e adiciona zero à esquerda se necessário
        mes = match.group(2)  # Captura o mês
        ano = match.group(3)  # Captura o ano
        return f"{ano}-{meses[mes]}-{dia} 14:00:00"
    else:
        raise ValueError("Formato de data inválido!")

url_base = 'https://buritiempreendimentos.com.br//blog/page/{}/'
num_paginas = 23
geral = []
site_base = 'https://buritiempreendimentos.com.br/'

for i in range(1, num_paginas + 1):
    url = url_base.format(i)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.find_all('article')  # Ajuste conforme a estrutura do site

        for post in posts:
            titulo_elem = post.find('h4', class_='post_title')
            imagem_elem = post.find('div', class_='post_featured')
            link_elem = post.find('a', href=True)
            data_elem = post.find('span', class_='post_date')

            titulo = titulo_elem.text.strip() if titulo_elem else 'Sem título'
            imagem = imagem_elem.find('img')['src'] if imagem_elem and imagem_elem.find('img') else 'Sem imagem'
            link_pagina_interna = link_elem['href'] if link_elem else None
            data_texto = data_elem.find('a').text.strip() if data_elem else None
            data = converter_data(data_texto)

            conteudo = 'Sem conteúdo'  # Valor padrão caso falhe a captura

            if link_pagina_interna:
                if not link_pagina_interna.startswith("http"):
                    link_pagina_interna = site_base + link_pagina_interna  # Garante que a URL seja absoluta

                response_interna = requests.get(link_pagina_interna)

                if response_interna.status_code == 200:
                    soup_interna = BeautifulSoup(response_interna.text, 'html.parser')

                    # Busca o conteúdo na página interna corretamente
                    conteudo_elem = soup_interna.find('div', class_='post_content')

                    if conteudo_elem:
                        conteudo = conteudo_elem.decode_contents()  # Mantém a estrutura HTML
                    else:
                        print(f"Div não encontrada na {link_pagina_interna}")
                else:
                    print(f"Erro ao acessar {link_pagina_interna}, status code: {response_interna.status_code}")

            item = {
                'titulo': titulo,
                'imagem': imagem,
                'data': data,
                'link': link_pagina_interna,
                'conteudo': conteudo,
            }

            print(item)
            geral.append(item)
    else:
        print(f'Erro ao acessar {url}, status code: {response.status_code}')


# # Salvando os dados coletados em um arquivo JSON
with open('C:/Users/igorj/OneDrive/Documentos/Code/Automações/BURITIDecoded.json', 'w', encoding='utf-8') as f:
    json.dump(geral, f, ensure_ascii=False, indent=4)

print("Dados salvos com sucesso!")
