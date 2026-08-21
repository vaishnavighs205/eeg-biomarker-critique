from pathlib import Path

import mne


EXPECTED_CHANNELS = {
    "Fp1",
    "Fp2",
    "F3",
    "F4",
    "C3",
    "C4",
    "P3",
    "P4",
    "O1",
    "O2",
    "F7",
    "F8",
    "T3",
    "T4",
    "T5",
    "T6",
    "Fz",
    "Cz",
    "Pz",
}


def get_eeg_path(
    dataset_root: str | Path,
    subject_id: str,
) -> Path:
    """Return the cleaned derivative EEG path for a subject."""

    dataset_root = Path(dataset_root)

    return (
        dataset_root
        / "derivatives"
        / subject_id
        / "eeg"
        / f"{subject_id}_task-eyesclosed_eeg.set"
    )


def load_subject_eeg(
    dataset_root: str | Path,
    subject_id: str,
    preload: bool = False,
):
    """
    Load one cleaned EEG recording from ds004504.
    """

    eeg_path = get_eeg_path(dataset_root, subject_id)

    if not eeg_path.exists():
        raise FileNotFoundError(
            f"EEG data unavailable for {subject_id}: {eeg_path}\n"
            "If this is a DataLad dataset, run:\n"
            f"datalad get {eeg_path}"
        )

    raw = mne.io.read_raw_eeglab(
        eeg_path,
        preload=preload,
        verbose="ERROR",
    )

    return raw