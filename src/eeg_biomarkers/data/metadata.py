from pathlib import Path
import pandas as pd


def load_participants(dataset_root: str | Path, participants_tsv: str = "participants.tsv") -> pd.DataFrame:
    """Load participant metadata from the BIDS participants table."""
    path = Path(dataset_root) / participants_tsv
    if not path.exists():
        raise FileNotFoundError(f"participants.tsv not found: {path}")
    return pd.read_csv(path, sep="\t")
