from pathlib import Path
import mne


def load_eeglab_set(path: str | Path, preload: bool = False):
    """Load an EEGLAB .set recording with MNE."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    return mne.io.read_raw_eeglab(path, preload=preload, verbose="ERROR")
