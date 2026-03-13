import logging
import os

from config import LOG_FILE_PATH


# If logs folder does not exist, create it.
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

# Create logger.
logger = logging.getLogger("baseball_etl")
logger.setLevel(logging.INFO)

if not logger.handlers:
    # Create file handler and formatter for pipeline logs.
    file_handler = logging.FileHandler(LOG_FILE_PATH)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def get_logger() -> logging.Logger:
    return logger


