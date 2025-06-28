import os
import logging

log_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'All_Logs')
os.makedirs(log_dir, exist_ok=True)

log_file_path = os.path.join(log_dir, 'load_logs.log')

load_logger = logging.getLogger("loading_logger")
load_logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s : %(filename)s : %(lineno)d')

file_handler = logging.FileHandler(log_file_path, mode='a')
file_handler.setFormatter(formatter)

load_logger.addHandler(file_handler)

if not load_logger.hasHandlers():
    load_logger.addHandler(file_handler)