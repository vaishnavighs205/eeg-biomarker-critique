from pathlib import Path

import pandas as pd

from eeg_biomarkers.data.metadata import load_participants
from eeg_biomarkers.data.load_eeg import load_subject_eeg
from eeg_biomarkers.preprocessing.epoch import get_epoch_windows


ROOT = Path(__file__).resolve().parents[1]

DATASET_ROOT = ROOT / "data" / "ds004504"

OUTPUT_DIR = ROOT / "results" / "tables"
OUTPUT_FILE = OUTPUT_DIR / "epoch_manifest.csv"


EPOCH_DURATION = 30.0
EPOCH_OVERLAP = 15.0


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    participants = load_participants(DATASET_ROOT)

    rows = []

    print("=" * 60)
    print("Building EEG epoch manifest")
    print("=" * 60)

    for i, participant in participants.iterrows():

        subject_id = participant["subject_id"]

        print(
            f"[{i + 1:02d}/{len(participants)}] "
            f"{subject_id}",
            end=" ",
            flush=True,
        )

        raw = load_subject_eeg(
            DATASET_ROOT,
            subject_id,
            preload=False,
        )

        windows = get_epoch_windows(
            raw,
            duration=EPOCH_DURATION,
            overlap=EPOCH_OVERLAP,
        )

        print(f"{len(windows)} epochs")

        for window in windows:

            rows.append(
                {
                    "subject_id": subject_id,
                    "diagnosis": participant["diagnosis"],
                    "age": participant["age"],
                    "sex": participant["sex"],
                    "mmse": participant["mmse"],

                    "epoch_id": window["epoch_id"],
                    "start_s": window["start_s"],
                    "end_s": window["end_s"],

                    "duration_s": EPOCH_DURATION,
                    "overlap_s": EPOCH_OVERLAP,
                }
            )

    manifest = pd.DataFrame(rows)

    manifest.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("\n" + "=" * 60)
    print("EPOCH MANIFEST COMPLETE")
    print("=" * 60)

    print(
        f"\nTotal EEG windows: "
        f"{len(manifest)}"
    )

    print(
        f"Independent subjects: "
        f"{manifest['subject_id'].nunique()}"
    )

    print("\nWindows by diagnosis:")

    print(
        manifest.groupby("diagnosis")
        .size()
    )

    print("\nEpochs per subject:")

    print(
        manifest.groupby("subject_id")
        .size()
        .describe()
    )

    print(
        f"\nSaved to:\n{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()