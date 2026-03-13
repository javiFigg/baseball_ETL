import sys
import os

from config import Config
from extractor import CSVExtractor
from transformer import DataTransformer
from validator import DataValidator
from loader import SQLLoader
from pipeline import ETLPipeline

# Ensure src is in the Python path when running from project root.
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

def main():
    config = Config()
    extractor = CSVExtractor(
        file_path=config.csv_file_path,
        columns_to_keep=config.columns_to_keep,
        chunk_size=config.chunk_size,
    )
    loader = SQLLoader(config.database_path)
    pipeline = ETLPipeline(
        extractor=extractor,
        transformer_class=DataTransformer,
        validator_class=DataValidator,
        loader=loader,
        table_name=config.table_name,
    )
    pipeline.run(
        required_columns=config.required_columns,
        numeric_columns=config.numeric_columns,
    )

if __name__ == "__main__":
    main()

