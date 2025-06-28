import os
from app.logging.transformation_logger import transformation_logger
from app.load.run_sql_scripts import run_sql_scripts

def populate_script_check(db_conn, script_file_path, script_name, schema_name):

    try:
        cursor = db_conn.cursor()
        table_name = script_name.replace("Populate", "")
        cursor.execute(f"SELECT COUNT(*) FROM {schema_name}.{table_name}")
        transformation_logger.info(f"Checking if {table_name} table is populated...")
        row_count = cursor.fetchone()
        row_count = int(row_count[0])
        if row_count == 0:
            print(f"Populating {table_name} table...")
            transformation_logger.info(f"Populating {table_name} table...")
            run_sql_scripts(db_conn, script_file_path)
            transformation_logger.info(f"{script_name} completed successfully.")
            print(f"{script_name} completed successfully.")

        else:
            print(f"{script_name} already populated. Skipping populate script.")
            transformation_logger.info(f"{script_name} already populated. Skipping populate script.")
    except Exception as e:
        transformation_logger.error(f"An error occurred: {e}")
        print(f"\033[91mAn error occurred, see logs for more details transformation_logs.\033[0m")