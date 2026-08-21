from pathlib import Path

import pandas as pd


GROUP_MAP = {
    "A": "AD",
    "F": "FTD",
    "C": "CN",
}


def load_participants(dataset_root: str | Path) -> pd.DataFrame:
    """
    Load and standardize ds004504 participant metadata.

    Parameters
    ----------
    dataset_root
        Root directory of the ds004504 dataset.

    Returns
    -------
    pd.DataFrame
        Participant metadata with standardized diagnosis labels.
    """
    dataset_root = Path(dataset_root)
    participants_file = dataset_root / "participants.tsv"

    if not participants_file.exists():
        raise FileNotFoundError(
            f"participants.tsv not found at: {participants_file}"
        )

    df = pd.read_csv(participants_file, sep="\t")

    required_columns = {
        "participant_id",
        "Gender",
        "Age",
        "Group",
        "MMSE",
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"participants.tsv is missing required columns: {missing}"
        )

    df = df.rename(
        columns={
            "participant_id": "subject_id",
            "Gender": "sex",
            "Age": "age",
            "Group": "group_code",
            "MMSE": "mmse",
        }
    )

    df["diagnosis"] = df["group_code"].map(GROUP_MAP)

    if df["diagnosis"].isna().any():
        bad_labels = df.loc[
            df["diagnosis"].isna(), "group_code"
        ].unique()

        raise ValueError(
            f"Unknown diagnostic group labels: {bad_labels}"
        )

    return df[
        [
            "subject_id",
            "diagnosis",
            "group_code",
            "sex",
            "age",
            "mmse",
        ]
    ]