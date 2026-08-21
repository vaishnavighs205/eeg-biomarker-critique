import numpy as np
import mne


def create_fixed_epochs(
    raw: mne.io.BaseRaw,
    duration: float = 30.0,
    overlap: float = 15.0,
) -> mne.Epochs:
    """
    Split continuous EEG into fixed-length overlapping epochs.

    Parameters
    ----------
    raw
        Continuous MNE Raw EEG object.
    duration
        Epoch duration in seconds.
    overlap
        Overlap between consecutive epochs in seconds.

    Returns
    -------
    mne.Epochs
        Fixed-length EEG epochs.
    """

    if overlap >= duration:
        raise ValueError("overlap must be smaller than duration")

    events = mne.make_fixed_length_events(
        raw,
        start=0,
        stop=None,
        duration=duration - overlap,
    )

    epochs = mne.Epochs(
        raw,
        events,
        event_id={"rest": 1},
        tmin=0,
        tmax=duration - 1 / raw.info["sfreq"],
        baseline=None,
        preload=False,
        reject_by_annotation=True,
        verbose="ERROR",
    )

    return epochs


def get_epoch_windows(
    raw: mne.io.BaseRaw,
    duration: float = 30.0,
    overlap: float = 15.0,
):
    """
    Return start/end times for valid fixed-length epochs.
    """

    step = duration - overlap
    total_duration = raw.times[-1]

    starts = np.arange(
        0,
        total_duration - duration + 1e-9,
        step,
    )

    return [
        {
            "epoch_id": i,
            "start_s": float(start),
            "end_s": float(start + duration),
        }
        for i, start in enumerate(starts)
    ]