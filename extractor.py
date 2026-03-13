import pandas as pd

from config import RAW_FILE_PATH, COLUMNS_TO_KEEP, CHUNK_SIZE

class CSVExtractor:
    def __init__(self, file_path: str = RAW_FILE_PATH, columns_to_keep: list = COLUMNS_TO_KEEP, chunk_size: int = CHUNK_SIZE):
        self.file_path = file_path
        self.columns_to_keep = columns_to_keep
        self.chunk_size = chunk_size

    def extract(self) -> pd.DataFrame:
        """Extracts data from the CSV file in chunks and concatenates them into a single DataFrame."""
        chunks = []
        for chunk in pd.read_csv(self.file_path, usecols=self.columns_to_keep, chunksize=self.chunk_size):
            chunks.append(chunk)
        return pd.concat(chunks, ignore_index=True)

    def extract_in_chunks(self):
        """Yields DataFrame chunks as (chunk_number, chunk)."""
        for chunk_number, chunk in enumerate(
            pd.read_csv(self.file_path, usecols=self.columns_to_keep, chunksize=self.chunk_size),
            start=1,
        ):
            yield chunk_number, chunk