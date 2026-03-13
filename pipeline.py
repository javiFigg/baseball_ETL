from logger import get_logger

logger = get_logger()

class ETLPipeline:
    def __init__(self, extractor, transformer_class, validator_class, loader, table_name):
        self.extractor = extractor
        self.transformer_class = transformer_class
        self.validator_class = validator_class
        self.loader = loader
        self.table_name = table_name

    def run(self, required_columns=None, numeric_columns=None):
        logger.info("Pipeline started")

        first_chunk = True

        for chunk_number, chunk in self.extractor.extract_in_chunks():
            logger.info(f"Processing chunk number {chunk_number}")

            transformer = self.transformer_class(chunk)
            transformed_chunk = transformer.transform()

            validator = self.validator_class(transformed_chunk)
            if not validator.validate(required_columns=required_columns, numeric_columns=numeric_columns):
                logger.warning(f"Chunk {chunk_number} failed validation")
                continue

            mode = "replace" if first_chunk else "append"

            self.loader.load_chunk(transformed_chunk, self.table_name, mode)

            logger.info(f"Rows loaded for chunk {chunk_number}: {len(transformed_chunk)}")

            first_chunk = False

        logger.info("Pipeline completed")