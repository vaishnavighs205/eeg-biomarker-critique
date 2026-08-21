from pathlib import Path
import mne

# Repository root
ROOT = Path(__file__).resolve().parents[1]

file = (
    ROOT
    / "data"
    / "ds004504"
    / "derivatives"
    / "sub-001"
    / "eeg"
    / "sub-001_task-eyesclosed_eeg.set"
)

print("Looking for EEG file at:")
print(file)

if not file.exists():
    raise FileNotFoundError(
        f"\nEEG file not found:\n{file}\n"
        "Make sure ds004504 has been downloaded into data/ds004504."
    )

raw = mne.io.read_raw_eeglab(file, preload=False)

print("\nSuccessfully loaded EEG!")
print(raw)
print("\nSampling frequency:", raw.info["sfreq"], "Hz")
print("Number of channels:", len(raw.ch_names))
print("Channels:", raw.ch_names)
print("Duration:", raw.times[-1], "seconds")