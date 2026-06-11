"""Download the Oracle's Elixir 2022 LoL esports match dataset.

The dataset is published by Tim "Magic" Sevenhuysen on https://oracleselixir.com
and hosted on Google Drive. We use ``gdown`` to handle Google Drive's
large-file confirmation flow.
"""
from __future__ import annotations

import sys
from pathlib import Path

import gdown

# Google Drive file id for the 2022 match-data CSV (see oracleselixir.com/tools/downloads).
DRIVE_FILE_ID = "1EHmptHyzY8owv0BAcNKtkQpMwfkURwRy"
DATA_DIR = Path(__file__).parent / "data"
CSV_PATH = DATA_DIR / "2022_LoL_esports_match_data_from_OraclesElixir.csv"


def download(force: bool = False) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if CSV_PATH.exists() and not force:
        print(f"Dataset already present at {CSV_PATH} ({CSV_PATH.stat().st_size:,} bytes).")
        return CSV_PATH
    print("Downloading 2022 Oracle's Elixir match data...")
    gdown.download(id=DRIVE_FILE_ID, output=str(CSV_PATH), quiet=False)
    print(f"Saved to {CSV_PATH}.")
    return CSV_PATH


if __name__ == "__main__":
    download(force="--force" in sys.argv)
