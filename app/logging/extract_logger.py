import os
import logging

log_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'All_Logs')
os.makedirs(log_dir, exist_ok=True)

log_file_path = os.path.join(log_dir, 'extraction_logs.log')

extract_logger = logging.getLogger("extraction_logger")
extract_logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s : %(filename)s : %(lineno)d')

file_handler = logging.FileHandler(log_file_path, mode='a')
file_handler.setFormatter(formatter)

extract_logger.addHandler(file_handler)

if not extract_logger.hasHandlers():
    extract_logger.addHandler(file_handler)