import sys
import os

from config import Config
from extractor import CSVExtractor
from transformer import DataTransformer
from validator import DataValidator
from loader import SQLLoader
from pipeline import ETLPipeline
from visualizer import DataVisualizer

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

    # Show visual insights from the finalized data in SQLite.
    visualizer = DataVisualizer(config.database_path)
    print("Opening chart: top pitchers by average release speed...")
    visualizer.plot_top_pitchers_by_release_speed(config.table_name)
    print("Opening chart: release speed distribution...")
    visualizer.visualize_release_speed_distribution(config.table_name)
    selected_player = visualizer.pick_player_name(
        config.table_name,
        preferred_name="Jacob deGrom",
    )
    if selected_player:
        print(f"Opening chart: release speed over time for {selected_player}...")
        visualizer.visualize_release_speed_over_time(config.table_name, player_name=selected_player)
    else:
        print("Skipping release speed over time chart: no valid player names found.")
    

if __name__ == "__main__":
    main()

