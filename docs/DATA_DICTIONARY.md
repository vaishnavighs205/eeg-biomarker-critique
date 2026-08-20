# Data Dictionary

## Subject metadata table

Suggested file: `data/processed/subjects.parquet`

| Column | Type | Description |
|---|---|---|
| subject_id | string | BIDS participant identifier |
| diagnosis | category | AD, FTD or CN |
| age | float | Participant age if available |
| sex | category | Participant sex metadata if available |
| mmse | float | Mini-Mental State Examination score |
| duration_s | float | Usable EEG recording duration |
| sfreq_hz | float | Sampling frequency |
| n_channels | int | Number of EEG channels loaded |
| qc_pass | bool | Overall QC decision |
| qc_notes | string | Human-readable QC comments |

## Epoch table

Suggested file: `data/processed/epochs_index.parquet`

| Column | Type | Description |
|---|---|---|
| subject_id | string | Participant identifier |
| epoch_id | int | Epoch index within subject |
| start_s | float | Epoch start time |
| stop_s | float | Epoch stop time |
| diagnosis | category | AD, FTD or CN |
| include | bool | Epoch inclusion flag |

## Feature table

Use a long or wide format, but always retain `subject_id` and `epoch_id` when epoch-level features are stored.

Recommended long-format columns:

| Column | Description |
|---|---|
| subject_id | Participant ID |
| epoch_id | Epoch ID or null for subject-level summary |
| channel | Electrode name |
| feature_family | e.g. RBP, specparam, wPLI |
| feature_name | e.g. alpha_relative_power |
| band | Optional frequency band |
| value | Numeric feature value |
