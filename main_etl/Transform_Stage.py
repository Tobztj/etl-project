import os
from configparser                                       import ConfigParser
from app.load.staging_load                              import load_staging_data
from app.load.populate_check                            import populate_script_check
from app.load.run_sql_scripts                           import run_sql_scripts
from app.logging.transformation_logger                  import transformation_logger
from app.transformations.data_cleaning.data_cleaning    import clean_data


def transform_stage(df, db_conn):

    # Load configuration from config.ini

    config = ConfigParser()
    config.read('config.ini')
    transformtion_dir = config['file_paths']['transformation_dir']

    #Step 3: Cleaning and transforming data
    try:
        transformation_logger.info("Cleaning and transforming data...")
        print("Cleaning and transforming data...")
        new_df = clean_data(df)
        transformation_logger.info("Data cleaning completed successfully.")
        print("Data cleaning completed successfully.")
        load_staging_data(df=new_df, connection=db_conn, schema_name='Staging', table_name='Policies')
        valid = True
    except Exception as e:
        transformation_logger.error(f"An error occurred: {e}")
        print(f"\033[91mAn error occurred, see logs for more details transformation_logs.\033[0m")
        valid = False


    for transform_obj in os.listdir(transformtion_dir):
        schema_name = transform_obj
        transformation_logger.info(f"{schema_name} Layer")

        for transform_type in os.listdir(os.path.join(transformtion_dir, transform_obj)):
            if transform_type == 'populate_script':
                script_path = os.path.join(transformtion_dir, transform_obj, 'populate_script')
                for script in os.listdir(script_path):
                    if script.endswith('.sql'):
                        script_file_path = os.path.join(script_path, script)
                        script_name = os.path.basename(script_file_path).replace('.sql', '')
                        populate_script_check(db_conn, script_file_path=script_file_path, schema_name=schema_name, script_name=script_name)
                        valid = True
                        continue
            elif transform_type == 'procedures':
                schema_proc_path = os.path.join(transformtion_dir, transform_obj, 'procedures')
                for proc in os.listdir(schema_proc_path):
                    if proc.endswith('.sql'):
                        proc_file_path = os.path.join(schema_proc_path, proc)
                        proc_name = os.path.basename(proc_file_path).replace('.sql', '')
                        run_sql_scripts(connection=db_conn, sql_file_path=proc_file_path, procedure=proc_name, schema_name=schema_name)
                        valid = True
            else:
                valid = True
    db_conn.close()

    return valid
