import os
from app.logging.load_logger import load_logger

# Execute the SQL script

def run_sql_scripts(connection, sql_file_path, procedure=None,schema_name=None):

    sql_script_path = os.path.join(os.path.dirname(__file__), sql_file_path)

    cursor = connection.cursor()
    with open(sql_script_path, 'r') as sql_file:
                sql_query = sql_file.read()


    if not procedure:
        try:
            for query in sql_query.split(';'):
                query = query.strip()
                if query:
                    message = f"Executing SQL query"
                    cursor.execute(query)
                    load_logger.info(message)
                    print(message)
                    connection.commit()

                    # for message in cursor.messages:
                    #     prefix = "[Microsoft][ODBC SQL Server Driver][SQL Server]"
                    #     msg = message[1]
                    #     run_message = msg[len(prefix):].strip()
                    #     valid = True
        except Exception as err:
            load_logger.error(f"An error occurred: {err}")
            print(f"An error occurred: {err}")

    else:
        # For stored procedures, we need to use a different approach

        proc_check = cursor.execute("SELECT [name] FROM sys.objects WHERE type = 'P' AND [name] = ?", (procedure))

        proc_result = proc_check.fetchone()


        try:
            if not proc_result:
                cursor.execute(sql_query)
                message = f"Stored procedure {procedure} created successfully."
                load_logger.info(message)
                print(message)
                cursor.execute(f"EXEC {schema_name}.{procedure}")
                message = f"Stored procedure {procedure} executed successfully."
                load_logger.info(message)
                print(message)
                connection.commit()
            else:
                cursor.execute(f"EXEC {schema_name}.{procedure}")
                message = f"Stored procedure {procedure} executed successfully."
                load_logger.info(message)
                print(message)
                connection.commit()
        except Exception as err:
            load_logger.error(f"An error occurred: {err}")
            print(f"An error occurred: {err}")