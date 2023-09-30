#!/usr/bin/env python3

import os
import re
import requests
import json


def save_json_to_file(data, file_path):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def get_code_smells_from_sonar_cloud(files_list, files_root, sonarcloud_url, sonarcloud_api_token):
    code_smells = {}
    output_file = "./reponse.json"

    for file_path in files_list:
        # Remova os dois componentes mais a raiz do caminho
        file_names = [
            f"lucasasantana_firefox-ios:{os.path.relpath(file_path, files_root)}" for file_path in files_list]

        # Construa a URL da API do SonarCloud para obter os code smells do arquivo
        api_url = f"{sonarcloud_url}/api/issues/search?componentKeys={','.join(file_names)}&types=CODE_SMELL"
        print(api_url)

        # Faça a requisição à API do SonarCloud
        response = requests.get(
            api_url, headers={"Authorization": f"Bearer {sonarcloud_api_token}"})

        if response.status_code == 200:
            code_smells = response.json()
            # Salva o JSON em um arquivo
            save_json_to_file(code_smells, output_file)
            # Exibe todo o JSON retornado
            print(f"Resposta da API do SonarCloud salva em '{output_file}'")
            return code_smells
        else:
            print(
                f"Falha ao obter code smells para o arquivo {file_path}. Path: {file_names} Status code: {response.status_code}")
            # Print da mensagem de erro completa
            print(f"Mensagem de erro: {response.text}")

    return code_smells


def find_files_with_regex_patterns(repo_path, regex_patterns):
    # Verifique se o diretório do repositório existe
    if not os.path.exists(repo_path):
        raise FileNotFoundError(
            f"O diretório do repositório '{repo_path}' não existe.")

    # Dicionário para armazenar os arquivos correspondentes e suas contagens de padrões
    matching_files_with_counts = {}

    # Percorre recursivamente o diretório do repositório
    for root, _, files in os.walk(repo_path):
        for file_name in files:
            if file_name.endswith(".swift"):
                file_path = os.path.join(root, file_name)
                with open(file_path, "r") as file:
                    content = file.read()
                    file_counts = 0  # Dicionário para armazenar contagens de padrões neste arquivo
                    for pattern in regex_patterns:
                        file_counts += len(re.findall(pattern, content))

                    if file_counts:  # Se houver contagens, adiciona o arquivo e suas contagens ao dicionário
                        matching_files_with_counts[file_path] = file_counts

    return matching_files_with_counts


if __name__ == "__main__":
    # Substitua pelo caminho do seu repositório
    repo_path = "../trabalho/firefox-ios"
    regex_patterns = [
        r'\.isFeatureEnabled\('
    ]

    # Substitua pela URL do seu projeto no SonarCloud
    sonarcloud_url = "https://sonarcloud.io"
    # Substitua pelo seu token de API do SonarCloud
    sonarcloud_api_token = "725d94ac496ccbd6d20c7e827ccb3b1777b6c35b"

    matching_files = find_files_with_regex_patterns(repo_path,regex_patterns)

    if matching_files:
        print(f"{len(matching_files)} arquivos correspondentes aos padrões de regex:")
        for file in matching_files:
            print(f"Arquivo: {file}, count: {matching_files[file]}")

        code_smells = get_code_smells_from_sonar_cloud(list(matching_files.keys()),repo_path, sonarcloud_url, sonarcloud_api_token)

        if code_smells:
            print(
                f"Quantidade de arquivos com code smells: {len(code_smells)}")

        else:
            print("Nenhum code smell encontrado nos arquivos.")
    else:
        print("Nenhum arquivo corresponde aos padrões de regex.")
