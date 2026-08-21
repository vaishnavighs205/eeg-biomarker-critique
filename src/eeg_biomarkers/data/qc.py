from pathlib import Path

import numpy as np

from eeg_biomarkers.data.load_eeg import (
    EXPECTED_CHANNELS,
    get_eeg_path,
    load_subject_eeg,
)


EXPECTED_SFREQ = 500.0


def qc_subject(
    dataset_root: str | Path,
    subject_id: str,
) -> dict:
    """
    Run basic quality-control checks for one EEG subject.
    """

    eeg_path = get_eeg_path(dataset_root, subject_id)

    result = {
        "subject_id": subject_id,
        "file_available": False,
        "n_channels": None,
        "sampling_rate_hz": None,
        "duration_s": None,
        "missing_channels": None,
        "extra_channels": None,
        "has_nan": None,
        "flat_channels": None,
        "status": "FAIL",
        "error": "",
    }

    if not eeg_path.exists():
        result["error"] = "EEG file unavailable"
        return result

    result["file_available"] = True

    try:
        # Preload because NaN / variance checks require signal data.
        raw = load_subject_eeg(
            dataset_root,
            subject_id,
            preload=True,
        )

        result["n_channels"] = len(raw.ch_names)
        result["sampling_rate_hz"] = float(raw.info["sfreq"])
        result["duration_s"] = float(raw.times[-1])

        actual_channels = set(raw.ch_names)

        missing = sorted(EXPECTED_CHANNELS - actual_channels)
        extra = sorted(actual_channels - EXPECTED_CHANNELS)

        result["missing_channels"] = ",".join(missing)
        result["extra_channels"] = ",".join(extra)

        data = raw.get_data()

        result["has_nan"] = bool(np.isnan(data).any())

        # MNE stores EEG internally in volts.
        channel_std = np.std(data, axis=1)

        # Detect essentially constant channels.
        flat_threshold = 1e-10

        flat_channels = [
            raw.ch_names[i]
            for i, std in enumerate(channel_std)
            if std < flat_threshold
        ]

        result["flat_channels"] = ",".join(flat_channels)

        passed = (
            len(raw.ch_names) == 19
            and abs(raw.info["sfreq"] - EXPECTED_SFREQ) < 1e-6
            and not missing
            and not extra
            and not result["has_nan"]
            and not flat_channels
        )

        result["status"] = "PASS" if passed else "REVIEW"

    except Exception as exc:
        result["error"] = str(exc)

    return result