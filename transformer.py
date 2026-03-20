import numpy as np
import pandas as pd


class DataTransformer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def clean_column_names(self) -> pd.DataFrame:
        self.df.columns = self.df.columns.str.lower().str.replace(" ", "_")
        self.df.columns = self.df.columns.str.strip()
        return self.df

    def remove_duplicates(self) -> pd.DataFrame:
        self.df = self.df.drop_duplicates()
        return self.df

    def handle_missing_values(self) -> pd.DataFrame:
        self.df = self.df.fillna(self.df.mean(numeric_only=True))
        return self.df

    def convert_data_types(self) -> pd.DataFrame:
        self.df["pitch_type"] = self.df["pitch_type"].astype(str)
        self.df["game_date"] = pd.to_datetime(self.df["game_date"], errors="coerce")
        self.df["release_speed"] = pd.to_numeric(self.df["release_speed"], errors="coerce")
        self.df["release_pos_x"] = pd.to_numeric(self.df["release_pos_x"], errors="coerce")
        self.df["release_pos_z"] = pd.to_numeric(self.df["release_pos_z"], errors="coerce")
        self.df["player_name"] = self.df["player_name"].astype(str)
        self.df["batter"] = self.df["batter"].astype(str)
        self.df["pitcher"] = self.df["pitcher"].astype(str)
        self.df["events"] = self.df["events"].astype(str)
        self.df["description"] = self.df["description"].astype(str)
        self.df["spin_dir"] = self.df["spin_dir"].astype(str)
        self.df["spin_rate_deprecated"] = pd.to_numeric(self.df["spin_rate_deprecated"], errors="coerce")
        return self.df

    def add_features(self) -> pd.DataFrame:
        if {
            "release_speed",
            "release_pos_x",
            "release_pos_z",
        }.issubset(self.df.columns):
            self.df["release_magnitude"] = np.sqrt(
                self.df["release_speed"] ** 2
                + self.df["release_pos_x"] ** 2
                + self.df["release_pos_z"] ** 2
            )

        if {"release_speed", "spin_rate_deprecated"}.issubset(self.df.columns):
            self.df["spin_efficiency"] = self.df["spin_rate_deprecated"] / self.df["release_speed"]
        return self.df

    def transform(self) -> pd.DataFrame:
        self.clean_column_names()
        self.remove_duplicates()
        self.handle_missing_values()
        self.convert_data_types()
        self.add_features()
        return self.df;