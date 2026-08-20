# Data Setup — OpenNeuro ds004504

## Canonical dataset source

This project uses the public OpenNeuro dataset:

- **Dataset:** `ds004504`
- **Snapshot DOI:** `10.18112/openneuro.ds004504.v1.0.9`
- **GitHub mirror:** `https://github.com/OpenNeuroDatasets/ds004504.git`
- **OpenNeuro snapshot:** `https://openneuro.org/datasets/ds004504/versions/1.0.9`

The upstream `dataset_description.json` identifies the current dataset as snapshot **v1.0.9**.

## Important: do not rely on plain `git clone` alone

The OpenNeuro GitHub mirror is a **DataLad/git-annex dataset**. Large EEG recordings are annexed rather than stored as ordinary Git blobs. In the GitHub tree, for example, derivative `.set` recordings appear as symlinks/pointers rather than the full EEG payload.

A plain:

```bash
git clone https://github.com/OpenNeuroDatasets/ds004504.git
```

is therefore useful for metadata and repository structure, but it may not populate the actual EEG recording content required by MNE.

## Recommended installation

Install DataLad and git-annex:

```bash
conda install -c conda-forge datalad git-annex
```

Then, from the root of this project, run:

```bash
bash scripts/get_ds004504.sh
```

The script installs the dataset at:

```text
data/ds004504/
```

and retrieves:

- `participants.tsv`
- `participants.json`
- `dataset_description.json`
- upstream `README`
- the complete `derivatives/` tree used for the primary analyses

You can choose a different destination:

```bash
bash scripts/get_ds004504.sh /absolute/path/to/ds004504
```

If you use a custom path, update `data.dataset_root` in `config.yaml` or create a local override.

## Why the derivative recordings are the starting point

The dataset authors provide both unprocessed subject recordings and denoised recordings under `derivatives/`. Their documented derivative pipeline includes:

1. Butterworth band-pass filtering from **0.5–45 Hz**
2. re-referencing to **A1–A2**
3. Artifact Subspace Reconstruction (ASR)
4. RunICA
5. automatic rejection of ICA components classified as eye or jaw artifacts by ICLabel

The primary replication/critique pipeline intentionally starts from these derivatives so the first analyses focus on the proposed biomarkers rather than differences in artifact-removal pipelines.

Raw-data preprocessing can later be added as a robustness experiment.

## Expected cohort

The upstream `participants.tsv` uses the following group codes:

| Upstream code | Project label | n |
|---|---|---:|
| `A` | AD | 36 |
| `F` | FTD | 23 |
| `C` | CN | 29 |
| **Total** |  | **88** |

Metadata columns available upstream are:

```text
participant_id
Gender
Age
Group
MMSE
```

Our metadata loader should map the upstream codes to explicit analysis labels:

```text
A -> AD
F -> FTD
C -> CN
```

Do not silently infer any other diagnosis labels.

## Expected EEG acquisition

The dataset documentation reports:

- resting-state, **eyes closed**
- **500 Hz** sampling rate
- 19 scalp electrodes
- international 10–20 montage
- referential recordings

Expected scalp channels:

```text
Fp1 Fp2 F7 F3 Fz F4 F8 T3 C3 Cz C4 T4 T5 P3 Pz P4 T6 O1 O2
```

The derivative file pattern is expected to resemble:

```text
derivatives/
└── sub-001/
    └── eeg/
        └── sub-001_task-eyesclosed_eeg.set
```

## Project configuration

The default repository configuration assumes:

```yaml
data:
  dataset_root: data/ds004504
  participants_tsv: participants.tsv
  use_derivatives: true
```

If the dataset is stored elsewhere, either edit `config.yaml` locally or use a non-tracked `config.local.yaml`.

## Structural checks before analysis

For every participant, confirm that:

- `participant_id` matches the EEG directory
- `Group` maps to exactly one of AD, FTD, or CN
- MMSE is parseable
- expected derivative EEG file exists
- sampling frequency is 500 Hz unless explicitly documented otherwise
- all 19 expected scalp electrodes are available
- channel names are standardized
- duration is nonzero and plausible
- values do not contain unexplained NaNs or infinities
- flat or extreme channels are recorded in the QC output

The analysis must stop rather than silently drop subjects when structural expectations fail.

## Data versioning

Record these fields in every analysis manifest:

```text
dataset = ds004504
snapshot = 1.0.9
DOI = 10.18112/openneuro.ds004504.v1.0.9
source_repo = https://github.com/OpenNeuroDatasets/ds004504.git
```

For stronger reproducibility, also save the upstream Git commit hash used for the local DataLad checkout.

## Data policy

The upstream dataset is marked **CC0**, but the EEG payload should still remain outside this project's Git history. Do not copy the OpenNeuro data into this repository's commits.

Commit only lightweight outputs such as:

- code
- documentation
- configuration
- aggregate feature tables where appropriate
- summary statistics
- figures
- model metadata

The local `data/ds004504/` directory is ignored by `.gitignore`.
