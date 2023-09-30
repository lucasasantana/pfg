import os
import re
from db import insert_file_and_flags

def find_files_with_regex_patterns(repo_path, files_root, regex_patterns, ignored_dirs):
    if not os.path.exists(repo_path):
        raise FileNotFoundError(f"O diretório do repositório '{repo_path}' não existe.")
    
    matching_files_with_counts = {}
    
    for root, dirs, files in os.walk(repo_path):
        # Exclui os diretórios ignorados da busca
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        
        for file_name in files:
            if file_name.endswith(".swift"):
                file_path = os.path.join(root, file_name)
                with open(file_path, "r") as file:
                    content = file.read()
                    total_matches = 0  # Contador total de correspondências para este arquivo
                    for pattern in regex_patterns:
                        total_matches += len(re.findall(pattern, content))
                    
                    matching_files_with_counts[os.path.relpath(file_path, files_root)] = total_matches
    
    return matching_files_with_counts

def save_to_sqlite(data):
    insert_file_and_flags(data)  # Fecha a conexão

if __name__ == "__main__":
    repo_path = "../trabalho/firefox-ios/Client"  # Substitua pelo caminho do seu repositório
    ignored_dirs = []

    regex_patterns = [
        r'\.isFeatureEnabled\('
    ]

    matching_files_with_counts = find_files_with_regex_patterns(repo_path, '../trabalho/firefox-ios', regex_patterns, ignored_dirs)

    if matching_files_with_counts:
        print(f"{len(matching_files_with_counts)} arquivos correspondentes aos padrões de regex:")
        for file_name, total_matches in matching_files_with_counts.items():
            print(f"Arquivo: {file_name}, Total de Correspondências: {total_matches}")
        
        save_to_sqlite(matching_files_with_counts)
    else:
        print("Nenhum arquivo corresponde aos padrões de regex.")
