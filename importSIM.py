import requests
from bs4 import BeautifulSoup
import json

url_base = 'https://simincorporadora.com.br/blog/{}/'
num_paginas = 5
geral = []
site_base = 'https://simincorporadora.com.br'

for i in range(1, num_paginas + 1):
    url = url_base.format(i)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.find_all('article')  # Ajuste conforme a estrutura do site

        for post in posts:
            titulo_elem = post.find('h3', class_='elementor-post__title')
            imagem_elem = post.find('div', class_='elementor-post__thumbnail')
            link_elem = post.find('a', href=True)

            titulo = titulo_elem.text.strip() if titulo_elem else 'Sem título'
            imagem = imagem_elem.find('img')['src'] if imagem_elem and imagem_elem.find('img') else 'Sem imagem'
            link_pagina_interna = link_elem['href'] if link_elem else None

            conteudo = 'Sem conteúdo'  # Valor padrão caso falhe a captura

            if link_pagina_interna:
                if not link_pagina_interna.startswith("http"):
                    link_pagina_interna = site_base + link_pagina_interna  # Garante que a URL seja absoluta

                response_interna = requests.get(link_pagina_interna)

                if response_interna.status_code == 200:
                    soup_interna = BeautifulSoup(response_interna.text, 'html.parser')

                    # Busca o conteúdo na página interna corretamente
                    conteudo_elem = soup_interna.find('div', attrs={'data-widget_type': 'theme-post-content.default'})

                    if conteudo_elem:
                        conteudo = conteudo_elem.decode_contents()  # Mantém a estrutura HTML
                    else:
                        print(f"Div não encontrada na {link_pagina_interna}")
                else:
                    print(f"Erro ao acessar {link_pagina_interna}, status code: {response_interna.status_code}")

            item = {
                'titulo': titulo,
                'imagem': imagem,
                'link': link_pagina_interna,
                'conteudo': conteudo
            }

            print(item)
            geral.append(item)
    else:
        print(f'Erro ao acessar {url}, status code: {response.status_code}')


# # Salvando os dados coletados em um arquivo JSON
with open('C:/Users/igorj/OneDrive/Documentos/Code/Automações/SIMDecoded.json', 'w', encoding='utf-8') as f:
    json.dump(geral, f, ensure_ascii=False, indent=4)

print("Dados salvos com sucesso!")
