import os
import json
from db import save_code_smells
from issues import issues_from_dict, Issues ,TypeEnum, IssueSeverity

# Importe as definições de dados e funções do seu arquivo anterior, como "Issues" e "issues_from_dict"

def load_data_from_json(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        print(f"Arquivo JSON não encontrado em: {file_path}")
        return None
    
def count_code_smells(values: Issues):
    # Implemente a lógica para contar os "code smells" no objeto issue
    # Por exemplo, você pode percorrer os flows e contar as ocorrências de code smells
    smells = {}
    for issue in values.issues:
        if not (issue.type == TypeEnum.CODE_SMELL): 
            continue

        component = issue.component.replace('lucasasantana_firefox-ios:', '')
        severity = issue.severity.value.lower()

        if not component in smells:
            smells[component] = {case.value.lower(): 0 for case in IssueSeverity}

        smells[component][severity] += (len(issue.flows) if len(issue.flows) > 0 else 1)

    return smells

def update_database_with_code_smells(data):
    save_code_smells(count_code_smells(data)) # Fecha a conexão

if __name__ == "__main__":
    json_file_paths = "./results/sonarcloud"  # Substitua pelo caminho do seu arquivo JSON
    

    for root, dirs, files in os.walk(json_file_paths):
        for file_name in files:
            if file_name.endswith(".json"):
                file_path = os.path.join(root, file_name)
        
                data = load_data_from_json(file_path)

                if data:        
                    # Atualize o banco de dados com a contagem de "code smells"
                    update_database_with_code_smells(issues_from_dict(data))

                print(f"Arquivo {file_path} analisado")





