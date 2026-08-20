# EEG Biomarker Critique & Minimal-Electrode Optimization

**Working title:** *Critical Evaluation and Minimal-Electrode Optimization of EEG Biomarkers for Alzheimer’s Disease*

This repository implements a reproducible BME + CS research pipeline for evaluating proposed EEG biomarkers of Alzheimer’s disease and determining whether the robust information can be preserved with a reduced scalp-electrode montage.

The project starts by reproducing the spectral and connectivity biomarkers used in **DICE-Net** on **OpenNeuro ds004504**, then systematically challenges their assumptions using individualized spectral analysis, periodic/aperiodic decomposition, alternative connectivity metrics, disease-specificity testing, cognitive-severity analysis, leakage-safe machine learning, and nested electrode selection.

## Core research questions

1. Can the Relative Band Power (RBP) and Spectral Coherence Connectivity (SCC) findings proposed in DICE-Net be reproduced?
2. Are fixed-band RBP findings stable when accounting for individual alpha frequency (IAF), absolute power, and the aperiodic 1/f component?
3. Are SCC findings stable when compared with connectivity metrics less sensitive to zero-lag coupling, such as wPLI and imaginary coherence?
4. Are the proposed biomarkers specific to Alzheimer’s disease, or do they also appear in frontotemporal dementia (FTD)?
5. Do candidate biomarkers correlate with cognitive severity measured by MMSE?
6. Which biomarker families contribute independent predictive value in subject-level machine-learning models?
7. What is the smallest electrode montage that preserves both classification performance and robust biomarker information?

## Dataset

- **Dataset:** OpenNeuro `ds004504`, version `1.0.9`
- **Recording:** resting-state, eyes-closed EEG
- **Sampling rate:** 500 Hz
- **Electrodes:** 19 scalp channels, standard 10–20 montage
- **Groups:** 36 AD, 23 FTD, 29 cognitively normal controls (88 total)
- **Metadata:** diagnosis, demographics, MMSE and related participant information
- **OpenNeuro:** https://openneuro.org/datasets/ds004504/versions/1.0.9
- **Upstream GitHub/DataLad repo:** https://github.com/OpenNeuroDatasets/ds004504.git

The repository expects the OpenNeuro dataset to remain outside version control. See [`docs/DATA_SETUP.md`](docs/DATA_SETUP.md).

## Scientific structure

```text
OpenNeuro ds004504
        |
        v
Dataset QC + metadata verification
        |
        v
Strict DICE-style replication
   |-- Relative Band Power (RBP)
   `-- Spectral Coherence Connectivity (SCC)
        |
        v
Biomarker critique
   |-- fixed vs individualized bands
   |-- relative vs absolute power
   |-- periodic vs aperiodic spectra
   |-- SCC vs wPLI / imaginary coherence
   |-- reference sensitivity
   |-- AD vs CN vs FTD specificity
   `-- MMSE association
        |
        v
Leakage-safe ML biomarker comparison
        |
        v
Robust biomarker set
        |
        v
Nested electrode selection
19 -> 12 -> 8 -> 6 -> 4 -> 2
        |
        v
Minimal biologically faithful montage
```

## Repository layout

```text
eeg-biomarker-critique/
├── README.md
├── config.yaml
├── requirements.txt
├── pyproject.toml
├── Makefile
├── docs/
├── data/
│   ├── raw/
│   ├── derivatives/
│   └── processed/
├── notebooks/
├── results/
│   ├── figures/
│   ├── tables/
│   ├── models/
│   └── logs/
├── scripts/
├── src/eeg_biomarkers/
└── tests/
```

## Quick start

### 1. Create the environment

```bash
conda create -n eeg_biomarkers python=3.11
conda activate eeg_biomarkers
pip install -r requirements.txt
pip install -e .
```

### 2. Retrieve the dataset

The upstream GitHub mirror uses **DataLad/git-annex**, so a plain `git clone` may not retrieve the EEG payload. Install DataLad/git-annex and use the included helper:

```bash
conda install -c conda-forge datalad git-annex
bash scripts/get_ds004504.sh
```

By default this installs the dataset under `data/ds004504/`, which already matches `config.yaml`. The project retrieves the provided cleaned `derivatives/` recordings first.

See [`docs/DATA_SETUP.md`](docs/DATA_SETUP.md) for the exact upstream structure, group-code mapping, and reproducibility notes.

Do **not** commit the EEG data to GitHub.

### 3. Verify the installation

```bash
python -m pytest
```

### 4. Run the first milestone

```bash
python scripts/run_qc.py --config config.yaml
```

The first milestone is complete only when all expected subjects can be matched to metadata and the EEG files pass basic structural QC.

## Validation rule that cannot be broken

**A subject is the independent sample.** EEG windows from the same person must never be split across training and test sets.

All transformations learned from data — scaling, feature selection, hyperparameter tuning, and electrode selection — must be fitted using training subjects only. See [`docs/VALIDATION.md`](docs/VALIDATION.md).

## Initial feature families

### DICE-style replication
- Relative delta power: 0.5–4 Hz
- Relative theta power: 4–8 Hz
- Relative alpha power: 8–13 Hz
- Relative beta power: 13–25 Hz
- Relative gamma power: 25–45 Hz
- Spectral coherence connectivity

### Critique / alternative features
- Absolute log band power
- Individual alpha frequency (IAF)
- Individualized frequency bands
- Periodic alpha peak frequency, amplitude and bandwidth
- Aperiodic exponent and offset
- wPLI / debiased wPLI
- Imaginary coherence
- Optional complexity features after the primary analyses are stable

## Initial models

The first ML comparisons intentionally favor small-data, interpretable models:

- Logistic regression
- Linear SVM
- XGBoost as a nonlinear comparison

Deep-learning models are optional extensions, not the starting point.

## Main evaluation metrics

- Balanced accuracy
- ROC-AUC
- Sensitivity
- Specificity
- F1 score
- Matthews correlation coefficient (MCC)
- Effect sizes and FDR-adjusted statistical tests for biomarker analyses

## Project milestones

1. Dataset setup and QC
2. RBP + SCC replication
3. Spectral biomarker critique
4. Connectivity biomarker critique
5. AD / FTD specificity and MMSE analysis
6. Leakage-safe ML biomarker comparison
7. Robust biomarker definition
8. Minimal-electrode optimization
9. Final figures, interpretation and documentation

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for the full sequence.

## Important interpretation boundary

Scalp EEG does **not** directly measure synapses. Aperiodic, oscillatory and connectivity measures may be discussed as electrophysiological markers associated with cortical circuit or synaptic/network dysfunction only when supported by the literature. They should not be described as direct measurements of synaptic loss or E/I balance.

## Reference papers

- Miltiadous A, et al. **DICE-Net: A Novel Convolution-Transformer Architecture for Alzheimer Detection in EEG Signals.** IEEE. https://ieeexplore.ieee.org/document/10179900
- OpenNeuro dataset `ds004504`: https://openneuro.org/datasets/ds004504/versions/1.0.9

## Status

Repository scaffold created. The next implementation task is **data loading + metadata matching + QC**, before any biomarker or ML analysis.
