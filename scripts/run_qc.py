from pathlib import Path

import pandas as pd

from eeg_biomarkers.data.metadata import load_participants
from eeg_biomarkers.data.qc import qc_subject


ROOT = Path(__file__).resolve().parents[1]

DATASET_ROOT = ROOT / "data" / "ds004504"

OUTPUT_DIR = ROOT / "results" / "tables"
OUTPUT_FILE = OUTPUT_DIR / "dataset_qc.csv"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    participants = load_participants(DATASET_ROOT)

    print("=" * 60)
    print("ds004504 EEG Dataset QC")
    print("=" * 60)

    print(f"\nParticipants: {len(participants)}")

    print("\nDiagnosis counts:")
    print(participants["diagnosis"].value_counts())

    qc_results = []

    for i, row in participants.iterrows():
        subject_id = row["subject_id"]

        print(
            f"[{i + 1:02d}/{len(participants)}] "
            f"Checking {subject_id}...",
            end=" ",
            flush=True,
        )

        result = qc_subject(
            DATASET_ROOT,
            subject_id,
        )

        result["diagnosis"] = row["diagnosis"]
        result["age"] = row["age"]
        result["sex"] = row["sex"]
        result["mmse"] = row["mmse"]

        qc_results.append(result)

        print(result["status"])

    qc_df = pd.DataFrame(qc_results)

    column_order = [
        "subject_id",
        "diagnosis",
        "age",
        "sex",
        "mmse",
        "file_available",
        "n_channels",
        "sampling_rate_hz",
        "duration_s",
        "missing_channels",
        "extra_channels",
        "has_nan",
        "flat_channels",
        "status",
        "error",
    ]

    qc_df = qc_df[column_order]

    qc_df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("\n" + "=" * 60)
    print("QC COMPLETE")
    print("=" * 60)

    print("\nStatus counts:")
    print(qc_df["status"].value_counts())

    print(
        f"\nMean recording duration: "
        f"{qc_df['duration_s'].mean() / 60:.2f} min"
    )

    print(
        f"Minimum recording duration: "
        f"{qc_df['duration_s'].min() / 60:.2f} min"
    )

    print(
        f"Maximum recording duration: "
        f"{qc_df['duration_s'].max() / 60:.2f} min"
    )

    print(f"\nQC table saved to:\n{OUTPUT_FILE}")


if __name__ == "__main__":
    main()