from __future__ import annotations

import numpy as np


def relative_band_power(freqs: np.ndarray, psd: np.ndarray, fmin: float, fmax: float,
                        total_fmin: float = 0.5, total_fmax: float = 45.0) -> np.ndarray:
    """Compute relative band power along the final PSD axis."""
    band = (freqs >= fmin) & (freqs < fmax)
    total = (freqs >= total_fmin) & (freqs <= total_fmax)
    band_power = np.trapz(psd[..., band], freqs[band], axis=-1)
    total_power = np.trapz(psd[..., total], freqs[total], axis=-1)
    return np.divide(band_power, total_power, out=np.full_like(band_power, np.nan, dtype=float), where=total_power != 0)
