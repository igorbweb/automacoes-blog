from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# URL do WordPress para adicionar novo post
url = "http://otimizacao1.aw8.com.br/labovet/wp-admin/post-new.php?post_type=exame"

# Lista de títulos dos posts que você deseja adicionar
titulos_posts = ["Título do Post 1", "Título do Post 2", "Título do Post 3"]

# Inicializa o driver do Selenium (usando o caminho do ChromeDriver)
driver = webdriver.Chrome()

# Restante do código permanece o mesmo...
