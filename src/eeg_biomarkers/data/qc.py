from __future__ import annotations

import numpy as np


def basic_raw_qc(raw, expected_channels: list[str]) -> dict:
    """Return lightweight structural QC information for an MNE Raw object."""
    available = list(raw.ch_names)
    missing = [ch for ch in expected_channels if ch not in available]
    duration_s = float(raw.n_times / raw.info["sfreq"])

    result = {
        "sfreq_hz": float(raw.info["sfreq"]),
        "n_channels": len(available),
        "duration_s": duration_s,
        "missing_channels": missing,
        "has_nonfinite": False,
    }

    # Avoid forcing a full long recording into memory unless already preloaded.
    if raw.preload:
        data = raw.get_data()
        result["has_nonfinite"] = bool(~np.isfinite(data).all())

    return result
