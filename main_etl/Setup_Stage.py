import os
from configparser                                       import ConfigParser
from app.logging.load_logger                            import load_logger
from app.load.create_database                           import create_database
from app.load.create_connection                         import database_connection
from app.load.check_schema_exists                       import check_schema_exists
from app.transformations.data_cleaning.data_cleaning    import clean_data


def setup_stage():

    config                      = ConfigParser()
    config.read('config.ini')
    DRIVER                      = config['database']['DRIVER']
    SERVER                      = config['database']['SERVER']
    DATABASE                    = config['database']['DATABASE']
    NEW_DATABASE                = config['database']['NEW_DATABASE']
    database_objects_dir        = config['file_paths']['database_objects_dir']

    #Step 2: Set up the database and objects
    load_logger.info(f"Setting up {NEW_DATABASE} ...")

    old_conn = database_connection(DRIVER, SERVER, DATABASE)
    if old_conn is None:
        print(f"\033[91mDatabase connection failed, see logs for more details load_logs.\033[0m")
        valid = False
    else:
        create_database(NEW_DATABASE, old_conn)
        valid = True
        old_conn.close()

    # Connect to the new database
    db_conn = database_connection(DRIVER, SERVER, NEW_DATABASE)
    if db_conn is None:
        print(f"\033[91mFailed to connect to {NEW_DATABASE}, see load_log for more details.\033[0m")
        load_logger.error(f"Failed to connect to {NEW_DATABASE}.")
        valid = False
    else:
        load_logger.info(f"Connected to {NEW_DATABASE} successfully.")
        print(f"Connected to {NEW_DATABASE} successfully.")
        valid = True



    for db_obj in os.listdir(database_objects_dir):
        schema_name = db_obj
        load_logger.info(f"{schema_name} Layer")
        schema_table_path = os.path.join(database_objects_dir, db_obj, 'tables')
        for table in os.listdir(schema_table_path):
            if table.endswith('.sql'):
                table_file_path = os.path.join(schema_table_path, table)
                table_name = os.path.basename(table_file_path).replace('.sql', '')
                try:
                    check_schema_exists(db_conn, schema_name, table_file_path, table_name)
                    valid = True
                except Exception as e:
                    load_logger.error(f"An error occurred: {e}")
                    print(f"\033[91mAn error occurred, see logs for more details load_logs.\033[0m")
                    valid = False

    return db_conn, valid
