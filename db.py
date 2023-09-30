import sqlite3
from issues import IssueSeverity


def create_connection():
    return sqlite3.connect("results/flags_data.sqlite")

def insert_file_and_flags(data):
    conn = create_connection()  # Conexão com o banco de dados SQLite
    cursor = conn.cursor()

    create_table_if_needed()

    for file_name, total_matches in data.items():
        cursor.execute("INSERT OR REPLACE INTO flags (file_name, number_of_flags) VALUES (?, ?)", (file_name, total_matches))

    conn.commit()  # Commit das alterações
    conn.close()    

def get_file_names():
    conn = create_connection()  # Conexão com o banco de dados SQLite
    cursor = conn.cursor()
    
    # Seleciona os nomes de arquivo da tabela
    cursor.execute("SELECT file_name FROM flags")
    files =  [row[0] for row in cursor.fetchall()]
    conn.close()

    return files

def create_table_if_needed():
    conn = create_connection()  # Conexão com o banco de dados SQLite
    cursor = conn.cursor()
    
    column_format = "{} INTEGER DEFAULT 0"
    columns = [column_format.format(case.name.lower()) for case in IssueSeverity]

    value = ",\n".join(columns)

    cursor.execute(
        f'''
        CREATE TABLE IF NOT EXISTS flags (
            file_name TEXT PRIMARY KEY,
            number_of_flags INTEGER,
            {value}
        )
        '''
    )

    conn.commit()  # Commit das alterações
    conn.close()

def save_code_smells(values):
    conn = create_connection()  # Conexão com o banco de dados SQLite
    cursor = conn.cursor()


    for component, smells_data in values.items():
        command = f"UPDATE flags SET {', '.join([f'{a} = ?' for a in smells_data.keys()])} WHERE file_name = ?"
        values_sql = tuple(list(map(str, smells_data.values())) + [component])

        cursor.execute(command, values_sql)

    conn.commit()  # Commit das alterações
    conn.close()  # Fecha a conexão

def fetch_all(query):
    conn = create_connection() 
    cursor = conn.cursor()

    # Executar a query
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return (results, cursor.description)

def fetch_one(query):
    conn = create_connection() 
    cursor = conn.cursor()

    # Executar a query
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    return result