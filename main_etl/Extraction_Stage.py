from configparser                           import ConfigParser
from app.extraction.get_file                import open_json_files
from app.logging.extract_logger             import extract_logger


def extraction_stage():

    # Load configuration from config.ini

    config                      = ConfigParser()
    config.read('config.ini')
    input_path                  = config['file_paths']['input_dir']
    output_path                 = config['file_paths']['test_output_dir']

    # Step 1: Extract data from JSON files
    try:
        extract_logger.info("Extracting data from JSON files...")
        print("Extracting files...")
        df = open_json_files(input_path, output_path)
        valid = True
    except Exception as e:
        extract_logger.error(f"An error occurred during the Extract Stage: {e}")
        print(f"\033[91mAn error occurred, see logs for more details extraction_logs\033[0m")
        valid = False

    return df, valid