#!/usr/bin/env python3
import argparse
from pathlib import Path

from eeg_biomarkers.config import load_config
from eeg_biomarkers.data.metadata import load_participants


def main() -> None:
    parser = argparse.ArgumentParser(description="Initial ds004504 metadata/QC entry point")
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    cfg = load_config(args.config)
    root = Path(cfg["data"]["dataset_root"])
    participants = load_participants(root, cfg["data"].get("participants_tsv", "participants.tsv"))

    print(f"Dataset root: {root}")
    print(f"Participants rows: {len(participants)}")
    print("Columns:", ", ".join(participants.columns))
    print("\nNext step: implement derivative EEG file discovery and per-subject structural QC.")


if __name__ == "__main__":
    main()
