from eeg_biomarkers.config import load_config
from eeg_biomarkers.preprocessing.epoch import epoch_parameters


def test_epoch_parameters():
    duration, step = epoch_parameters(30, 15)
    assert duration == 30
    assert step == 15


def test_config_loads():
    cfg = load_config("config.yaml")
    assert cfg["project"]["name"] == "eeg-biomarker-critique"
    assert cfg["data"]["expected_subjects"] == 88
