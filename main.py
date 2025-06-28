# # Script to run ETL pipeline for esure project
# import os
# from app.extraction.get_file import open_json_files
# from app.load.create_connection import database_connection
# from app.logging.extract_logger import extract_logger
# from app.logging.load_logger import load_logger
# from app.logging.transformation_logger import transformation_logger
# from app.load.run_sql_scripts import run_sql_scripts
# from app.load.check_schema_exists import check_schema_exists
# from app.load.staging_load import load_staging_data
# from app.load.create_database import create_database
# from app.transformations.data_cleaning.data_cleaning import clean_data
# from app.load.populate_check import populate_script_check
# from configparser import ConfigParser


# def run_etl_pipeline():

#     """
#     Main function to run the ETL pipeline.
#     """
#     # Load configuration from config.ini

#     config = ConfigParser()
#     config.read('config.ini')
#     output_path = config['file_paths']['test_output_dir']
#     input_path = config['file_paths']['input_dir']
#     schema_dir = config['file_paths']['schema_dir']
#     table_dir = config['file_paths']['table_dir']
#     database_objects_dir = config['file_paths']['database_objects_dir']
#     transformtion_dir = config['file_paths']['transformation_dir']
#     DRIVER = config['database']['DRIVER']
#     SERVER = config['database']['SERVER']
#     DATABASE= config['database']['DATABASE']
#     NEW_DATABASE = config['database']['NEW_DATABASE']


#     # Step 1: Extract data from JSON files
#     try:
#         extract_logger.info("Starting ETL pipeline...")
#         print("Starting ETL pipeline...")
#         extract_logger.info("Extracting data from JSON files...")
#         print("Extracting files...")
#         df = open_json_files(input_path, output_path)
#     except Exception as e:
#         extract_logger.error(f"An error occurred during the Extract Stage: {e}")
#         print(f"\033[91mAn error occurred, see logs for more details extraction_logs\033[0m")


#     # Step 2: Set up the database and objects
#     load_logger.info(f"Setting up {NEW_DATABASE} ...")

#     old_conn = database_connection(DRIVER, SERVER, DATABASE)
#     if old_conn is None:
#         print(f"\033[91mDatabase connection failed, see logs for more details load_logs.\033[0m")
#     else:
#         create_database( NEW_DATABASE, old_conn)
#         old_conn.close()

#     # Connect to the new database
#     db_conn = database_connection(DRIVER, SERVER, NEW_DATABASE)
#     if db_conn is None:
#         print(f"\033[91mFailed to connect to {NEW_DATABASE}, see load_log for more details.\033[0m")
#         load_logger.error(f"Failed to connect to {NEW_DATABASE}.")
#     else:
#         load_logger.info(f"Connected to {NEW_DATABASE} successfully.")
#         print(f"Connected to {NEW_DATABASE} successfully.")


#     for db_obj in os.listdir(database_objects_dir):
#         schema_name = db_obj
#         load_logger.info(f"{schema_name} Layer")
#         schema_table_path = os.path.join(database_objects_dir, db_obj, 'tables')
#         for table in os.listdir(schema_table_path):
#             if table.endswith('.sql'):
#                 table_file_path = os.path.join(schema_table_path, table)
#                 table_name = os.path.basename(table_file_path).replace('.sql', '')
#                 try:
#                     check_schema_exists(db_conn, schema_name, table_file_path, table_name)
#                 except Exception as e:
#                     load_logger.error(f"An error occurred: {e}")
#                     print(f"\033[91mAn error occurred, see logs for more details load_logs.\033[0m")

#     #Step 3: Cleaning and transforming data
#     try:
#         transformation_logger.info("Cleaning and transforming data...")
#         print("Cleaning and transforming data...")
#         new_df = clean_data(df)
#         transformation_logger.info("Data cleaning completed successfully.")
#         print("Data cleaning completed successfully.")
#         load_staging_data(new_df, db_conn, 'Staging', 'Policies')
#     except Exception as e:
#         transformation_logger.error(f"An error occurred: {e}")
#         print(f"\033[91mAn error occurred, see logs for more details transformation_logs.\033[0m")


#     for transform_obj in os.listdir(transformtion_dir):
#         schema_name = transform_obj
#         transformation_logger.info(f"{schema_name} Layer")

#         for transform_type in os.listdir(os.path.join(transformtion_dir, transform_obj)):
#             if transform_type == 'populate_script':
#                 script_path = os.path.join(transformtion_dir, transform_obj, 'populate_script')
#                 for script in os.listdir(script_path):
#                     if script.endswith('.sql'):
#                         script_file_path = os.path.join(script_path, script)
#                         script_name = os.path.basename(script_file_path).replace('.sql', '')
#                         populate_script_check(db_conn, script_file_path=script_file_path, schema_name=schema_name, script_name=script_name)
#                         continue
#             # elif transform_type == 'procedures':
#             #     schema_proc_path = os.path.join(transformtion_dir, transform_obj, 'procedures')
#             #     for proc in os.listdir(schema_proc_path):
#             #         if proc.endswith('.sql'):
#             #             proc_file_path = os.path.join(schema_proc_path, proc)
#             #             proc_name = os.path.basename(proc_file_path).replace('.sql', '')
#             #             run_sql_scripts(db_conn, proc_file_path, procedure=proc_name, schema_name=schema_name)
#             # else:
#             #     continue
#         #try:
#             # if not os.path.exists(schema_proc_path):
#             #     continue
#                     # Skip to the next folder if 'procedures' does not exist
#             #else:
#                 # for proc in os.listdir(schema_proc_path):
#                 #     if proc.endswith('.sql'):
#                 #         proc_file_path = os.path.join(schema_proc_path, proc)
#                 #         proc_name = os.path.basename(proc_file_path).replace('.sql', '')
#                 #         print(f"Executing stored procedure: {proc_name}")
#                 #         message = run_sql_scripts(db_conn, proc_file_path, procedure=proc_name, schema_name=schema_name)
#                 #         transformation_logger.info(f"{message}")
#                 #         print(message[1])
#         # except Exception as e:
#         #     transformation_logger.error(f"An error occurred: {e}")
#         #     print(f"\033[91mAn error occurred, see logs for more details transformation_logs.\033[0m")

#     db_conn.close()







#       # Test the connection
#     # Here you would typically call a function to load the extracted data into the database
#     # For example: load_data_to_db(db_conn, extracted_data)
# # print(output_path)
# #from app.extraction.file_validation import dict_validation

# # my_dict = {
# #     "policy_id": "POL-98584",
# #     "customer_id": "CUS-21441",
# #     "event_type": "purchase",
# #     "event_timestamp": "2024-06-30T20:41:32.163Z",
# #     "policy_type": "5",
# #     "premium_amount": 1788.19,
# #     "coverage_amount": 76782.39,
# #     "age_of_insured": 59,
# #     "region": "East"
# # }
# # dict_validation(my_dict)
# #open_json_files(input_path, output_path)
# run_etl_pipeline()
# # db_conn = database_connection(DRIVER, SERVER, DATABASE)
# # # Example usage of the database connection
# # sql = db_conn.execute("SELECT TOP 10 * FROM INFORMATION_SCHEMA.TABLES")
# # for row in sql.fetchall():
# #     print(row)
from main_etl.Setup_Stage             import setup_stage
from main_etl.Transform_Stage        import transform_stage
from main_etl.Extraction_Stage       import extraction_stage

def run_etl():

    print("Starting ETL pipeline...")

    # Step 1: Set up the environment
    db_conn, valid = setup_stage()
    if not valid:
        print("Set up failed. Please check the load_logs for details.")
    else:
        print("Set up completed successfully.")
        df, valid2 = extraction_stage()      # Step 2: Extract data
        if not valid2:
            print("Extraction stage failed. Please check the extraction_logs for details.")
        else:
            valid3 = transform_stage(df=df, db_conn=db_conn)   # Step 3: Transform & Load data
            if not valid3:
                print("Transformation stage failed. Please check the logs for details.")
            else:
                print("Transformation stage completed successfully.")
                print("ETL pipeline completed successfully.")
                print("You can now query the database for the transformed data.")


if __name__ == "__main__":
    run_etl()


