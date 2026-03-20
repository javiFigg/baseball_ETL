import sqlite3
import pandas as pd
import matplotlib.pyplot as plt  # Make sure matplotlib is installed: pip install matplotlib

class DataVisualizer:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def create_connection(self):
        """Creates a connection to the SQLite database."""
        return sqlite3.connect(self.db_path)

    def pick_player_name(self, table_name: str, preferred_name: str | None = None) -> str | None:
        """Returns a valid player name, preferring `preferred_name` when available."""
        conn = self.create_connection()
        try:
            if preferred_name:
                preferred_query = f"""
                SELECT player_name
                FROM {table_name}
                WHERE player_name = ?
                LIMIT 1
                """
                preferred_df = pd.read_sql_query(preferred_query, conn, params=(preferred_name,))
                if not preferred_df.empty:
                    return preferred_name

            fallback_query = f"""
            SELECT player_name
            FROM {table_name}
            WHERE player_name IS NOT NULL AND player_name != ''
            GROUP BY player_name
            ORDER BY RANDOM()
            LIMIT 1
            """
            fallback_df = pd.read_sql_query(fallback_query, conn)
            if fallback_df.empty:
                return None
            return str(fallback_df.iloc[0]["player_name"])
        finally:
            conn.close()
    
    def plot_top_pitchers_by_release_speed(self, table_name: str, top_n: int = 10):
        """Plots the top N player names by average release speed."""
        conn = self.create_connection()
        try:
            query = f"""
            SELECT player_name, AVG(release_speed) AS avg_release_speed
            FROM {table_name}
            WHERE player_name IS NOT NULL AND player_name != ''
            GROUP BY player_name
            ORDER BY avg_release_speed DESC
            LIMIT {top_n}
            """
            df = pd.read_sql_query(query, conn)
            plt.figure(figsize=(12, 8))
            plt.barh(df['player_name'], df['avg_release_speed'], color='orange')
            plt.title(f'Top {top_n} Players by Average Release Speed')
            plt.xlabel('Average Release Speed (mph)')
            plt.ylabel('Player Name')
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

    def visualize_release_speed_over_time(self, table_name: str, player_name: str):
        """Visualizes release speed over time for a specific player."""
        conn = self.create_connection()
        try:
            query = f"""
            SELECT game_date, release_speed
            FROM {table_name}
            WHERE player_name = ?
            ORDER BY game_date
            """
            df = pd.read_sql_query(query, conn, params=(player_name,))
            plt.figure(figsize=(12, 6))
            plt.plot(df['game_date'], df['release_speed'], marker='o', linestyle='-', color='green')
            plt.title(f'Release Speed Over Time for {player_name}')
            plt.xlabel('Game Date')
            plt.ylabel('Release Speed (mph)')
            plt.xticks(rotation=45)
            plt.grid()
            plt.show()
        finally:
            conn.close()
