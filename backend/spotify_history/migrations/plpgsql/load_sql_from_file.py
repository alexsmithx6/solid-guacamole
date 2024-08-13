import os

def load_sql_from_file(plpgsql_file):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{plpgsql_file}.sql')
    with open(path, 'r') as file:
        sql_query = file.read()
    return sql_query