import sqlite3
import pandas as pd
import matplotlib.pyplot as plt  # Make sure matplotlib is installed: pip install matplotlib

class DataVisualizer:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def create_connection(self):
        """Creates a connection to the SQLite database."""
        return sqlite3.connect(self.db_path)
    
    def plot_top_pitchers_by_release_speed(self, table_name: str, top_n: int = 10):
        """Plots the top N pitchers by average release speed."""
        conn = self.create_connection()
        try:
            query = f"""
            SELECT pitcher, AVG(release_speed) AS avg_release_speed
            FROM {table_name}
            GROUP BY pitcher
            ORDER BY avg_release_speed DESC
            LIMIT {top_n}
            """
            df = pd.read_sql_query(query, conn)
            plt.figure(figsize=(12, 8))
            plt.barh(df['pitcher'], df['avg_release_speed'], color='orange')
            plt.title(f'Top {top_n} Pitchers by Average Release Speed')
            plt.xlabel('Average Release Speed (mph)')
            plt.ylabel('Pitcher')
            plt.gca().invert_yaxis()  # Invert y-axis to show the highest at the top
            plt.grid(axis='x', alpha=0.75)
            plt.show()
        finally:
            conn.close()

    def visualize_release_speed_distribution(self, table_name: str):
        """Visualizes the distribution of release speeds using a histogram."""
        conn = self.create_connection()
        try:
            query = f"SELECT release_speed FROM {table_name}"
            df = pd.read_sql_query(query, conn)
            plt.figure(figsize=(10, 6))
            plt.hist(df['release_speed'], bins=30, color='blue', edgecolor='black')
            plt.title('Distribution of Release Speeds')
            plt.xlabel('Release Speed (mph)')
            plt.ylabel('Frequency')
            plt.grid(axis='y', alpha=0.75)
            plt.show()
        finally:
            conn.close()