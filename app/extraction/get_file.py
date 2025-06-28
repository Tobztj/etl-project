import os
import json
import pandas as pd
from app.extraction.file_validation import dict_validation
from app.logging.extract_logger import extract_logger


def open_json_files(folder_path,output_dir):

    data_list = [] # create a list to store all JSON objects from each file
    failed_records = []  # List to store records that fail validation
    data_list.clear()
    failed_records.clear()

    output_path = output_dir + r"\validation_failures.csv"

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        extract_logger.info(f"Output directory created: {output_dir}")


    if not os.path.exists(folder_path):
        extract_logger.error(f"Path does not exist: {folder_path}")
        print(f"Path does not exist: {folder_path}")


    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            extract_logger.info(f"Contents of {filename}:")
            with open(file_path, mode='r', encoding='utf-8') as f:
                for line_number, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        valid_record, invalid_record = dict_validation(data, filename, line_number)
                        if valid_record is True:
                            data['source_file'] = filename
                            data_list.append(data)
                            valid = True
                        else:
                            failed_records.extend(invalid_record)
                            valid = False
                    except json.JSONDecodeError as e:
                        extract_logger.error(f"Not a valid JSON: {line_number} in {filename}")
                        print(f"Error reading line {line_number} in {filename}: {e}")
    if valid:
        extract_logger.info(f"Validation complete")
        print(f"All File Validations complete")


    if failed_records:
        df_failed = pd.DataFrame(failed_records)
        df_failed.to_csv(output_path, mode='w', header=True, index=False)
        extract_logger.info(f"All failed validations exported to {output_path}")
        print(f"All failed validation and exported to {output_path}")

    if data_list:
        df = pd.DataFrame(data_list)
        extract_logger.info(f"Data Extract completed successfully")
        print(f"Data Extract completed successfully")
    else:
        extract_logger.warning("No valid JSON objects found in the provided files.")
        print("No valid JSON objects found in this file.")

    data_list.clear()
    failed_records.clear()


    return df