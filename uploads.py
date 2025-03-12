import os
import csv

def carregar_lista_arquivos(csv_path):
    """Lê um arquivo CSV e retorna uma lista com os nomes dos arquivos a serem buscados."""
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            return [row[0].strip() for row in reader if row]  # Remove espaços extras
    except FileNotFoundError:
        print(f"Erro: Arquivo CSV '{csv_path}' não encontrado.")
        return []

def buscar_arquivos(diretorio, lista_arquivos):
    """Percorre todas as subpastas do diretório e busca arquivos da lista."""
    encontrados = {}

    for root, _, files in os.walk(diretorio):  # Percorre todas as pastas e subpastas
        for file in files:
            if file in lista_arquivos:
                encontrados[file] = os.path.join(root, file)

    return encontrados

def salvar_resultados(resultados, output_csv):
    """Salva os arquivos encontrados em um novo CSV."""
    with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Arquivo", "Caminho Completo"])  # Cabeçalho
        for nome, caminho in resultados.items():
            writer.writerow([nome, caminho])

# === Configurações ===
diretorio_base = "C:/Users/igorj/Downloads/Buritis/BackupFinal/uploads"  # Diretório base
csv_lista_arquivos = "C:/Users/igorj/Downloads/Buritis/BackupFinal/uploads/midias.csv"  # Caminho do CSV contendo os arquivos a serem buscados
output_csv = "arquivos_encontrados.csv"  # Onde salvar os resultados encontrados

print(csv_lista_arquivos)

# === Execução ===
arquivos_procurados = carregar_lista_arquivos(csv_lista_arquivos)
if arquivos_procurados:
    resultado = buscar_arquivos(diretorio_base, arquivos_procurados)
    
    if resultado:
        salvar_resultados(resultado, output_csv)
        print(f"Arquivos encontrados e salvos em '{output_csv}'.")
    else:
        print("Nenhum arquivo da lista foi encontrado.")
else:
    print("Lista de arquivos vazia ou erro ao carregar o CSV.")