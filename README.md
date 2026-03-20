# Baseball Pipeline (ETL + Visualization)

This project processes baseball pitch data from CSV into SQLite using a chunked ETL pipeline, then generates charts from the finalized table.

## What This Project Does

- Extracts data from `baseball_ETL/baseball.csv` in chunks
- Transforms and validates each chunk
- Loads cleaned data into SQLite (`baseball_ETL/baseball.db`)
- Logs pipeline progress to file and console
- Visualizes:
  - Top players by average release speed
  - Release speed distribution histogram

## Project Structure

```text
Baseball_PIPELINE/
  baseball_ETL/
    baseball.csv
    config.py
    extractor.py
    transformer.py
    validator.py
    loader.py
    pipeline.py
    visualizer.py
    logger.py
    main.py
    baseball.db
    logs/
      pipeline.log
```

## Requirements

- Python 3.10+
- `pandas`
- `numpy`
- `matplotlib`

Install dependencies:

```powershell
py -m pip install pandas numpy matplotlib
```

## How To Run

Run from the `baseball_ETL` folder (important because config uses relative paths):

```powershell
Set-Location .\baseball_ETL
py .\main.py
```

You should see:

- Chunk-by-chunk logs in the terminal
- Pipeline logs appended to `logs/pipeline.log`
- Two chart windows after ETL completes

## Outputs

- Final database file: `baseball_ETL/baseball.db`
- Final table: `baseball_stats`
- Log file: `baseball_ETL/logs/pipeline.log`

Note: The pipeline does not create per-chunk output files. Chunks are processed in memory and loaded into SQLite.

## Config

Main settings are in `baseball_ETL/config.py`:

- `RAW_FILE_PATH = "baseball.csv"`
- `DB_PATH = "baseball.db"`
- `TABLE_NAME = "baseball_stats"`
- `LOG_FILE_PATH = "logs/pipeline.log"`
- `CHUNK_SIZE = 50000`

## Pipeline Flow

1. `CSVExtractor` reads CSV in chunks
2. `DataTransformer` cleans, normalizes, and adds features
3. `DataValidator` checks required and numeric columns
4. `SQLLoader` writes first chunk with `replace`, remaining chunks with `append`
5. `DataVisualizer` queries SQLite and displays charts

## Troubleshooting

### FileNotFoundError: `baseball.csv`

Cause: Running from the wrong working directory.

Fix:

```powershell
Set-Location .\baseball_ETL
py .\main.py
```

### No charts appear

- Ensure `matplotlib` is installed.
- Wait until ETL completes; charts open after data load.
- If running in a headless environment, configure a non-interactive backend or save plots to files.

## Notes

- Re-running the pipeline rebuilds the target table each run (first chunk uses `replace`).
