from app.load.run_sql_scripts import run_sql_scripts
from app.logging.load_logger import load_logger

def check_schema_exists(connection, schema_name, table_file_path, table_name):

    cursor = connection.cursor()

    schema_check = cursor.execute("SELECT schema_name FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = ?", (schema_name))
    schema_result = schema_check.fetchone()

    table_check = cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?", (schema_name, table_name))
    table_result = table_check.fetchone()

    try:
        if not schema_result:
            load_logger.info(f"Creating {schema_name} Schema.")
            print(f"Creating {schema_name} Schema.")
            cursor.execute(f"CREATE SCHEMA {schema_name}")
            load_logger.info(f"Creating {table_name} table.")
            print(f"Creating {table_name} table.")
            run_sql_scripts(connection, table_file_path)
            connection.commit()
        elif schema_result and not table_result:
            load_logger.info(f"Schema {schema_name} exists, but {table_name} table does not exist. Creating {table_name} table.")
            print(f"Schema {schema_name} exists, but {table_name} table does not exist. Creating {table_name} table.")
            run_sql_scripts(connection, table_file_path)
            connection.commit()
        else:
            load_logger.info(f"{schema_name} Schema and {schema_name}.{table_name} table already exists in the database.")
    except Exception as e:
        load_logger.error(f"An error: {e}")
        print(f"An error occurred: {e}")
