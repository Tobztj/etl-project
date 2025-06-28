import os
import logging

log_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'All_Logs')
os.makedirs(log_dir, exist_ok=True)

log_file_path = os.path.join(log_dir, 'transformation_logs.log')

transformation_logger = logging.getLogger("transformation_logger")
transformation_logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s : %(filename)s : %(lineno)d')

file_handler = logging.FileHandler(log_file_path, mode='a')
file_handler.setFormatter(formatter)

transformation_logger.addHandler(file_handler)

if not transformation_logger.hasHandlers():
    transformation_logger.addHandler(file_handler)