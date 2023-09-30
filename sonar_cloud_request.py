from db import get_file_names
import requests
import json

def divide_chunks(l, n):  
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]

def save_json_to_file(data, file_path):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

def get_code_smells_from_sonar_cloud(chunks, sonarcloud_url, sonarcloud_api_token):
    i = 0

    for files_list in chunks:
        i += 1
        output_file = f"./results/sonarcloud/reponse_{i}.json"

        # Remova os dois componentes mais a raiz do caminho
        file_names = [f"lucasasantana_firefox-ios:{file_path}" for file_path in files_list]

        # Construa a URL da API do SonarCloud para obter os code smells do arquivo
        api_url = f"{sonarcloud_url}/api/issues/search?componentKeys={','.join(file_names)}&types=CODE_SMELL"

        # Faça a requisição à API do SonarCloud
        response = requests.get(api_url, headers={"Authorization": f"Bearer {sonarcloud_api_token}"})

        if response.status_code == 200:
            save_json_to_file(response.json(), output_file)
            print(f"Resposta da API do SonarCloud salva em '{output_file}'")

        else:
            print(f"Falha ao obter code smells para o arquivos {file_names}. Path: {file_names} Status code: {response.status_code}")
            # Print da mensagem de erro completa
            print(f"Mensagem de erro: {response.text}")
    
    
    

if __name__ == "__main__":
    file_names = get_file_names()
    
    sonarcloud_url = "https://sonarcloud.io"  # Substitua pela URL do seu projeto no SonarCloud
    sonarcloud_api_token = "725d94ac496ccbd6d20c7e827ccb3b1777b6c35b"  # Substitua pelo seu token de API do SonarCloud

    get_code_smells_from_sonar_cloud(list(divide_chunks(file_names, 50)), sonarcloud_url, sonarcloud_api_token)  # Fecha a conexão
