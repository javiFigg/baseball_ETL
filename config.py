RAW_FILE_PATH = "baseball.csv"
DB_PATH = "baseball.db"
TABLE_NAME = "baseball_stats"
LOG_FILE_PATH = "logs/pipeline.log"
CHUNK_SIZE = 50000

COLUMNS_TO_KEEP = [
    "pitch_type", "game_date", "release_speed", 
    "release_pos_x", "release_pos_z", "player_name",
    "batter", "pitcher", "events", "description", "spin_dir",
    "spin_rate_deprecated", 
    ]


class Config:
    def __init__(self):
        self.csv_file_path = RAW_FILE_PATH
        self.database_path = DB_PATH
        self.table_name = TABLE_NAME
        self.log_file_path = LOG_FILE_PATH
        self.chunk_size = CHUNK_SIZE
        self.columns_to_keep = COLUMNS_TO_KEEP
        self.required_columns = COLUMNS_TO_KEEP
        self.numeric_columns = [
            "release_speed",
            "release_pos_x",
            "release_pos_z",
            "spin_rate_deprecated",
        ]
