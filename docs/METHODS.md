# Methods

## 1. Dataset QC

Create a subject-level QC table containing:

- subject ID
- diagnosis
- age
- sex
- MMSE
- recording duration
- sampling frequency
- channel count
- missing channels
- flat channels
- extreme amplitude flags
- inclusion/exclusion decision

QC decisions must be logged before examining downstream model performance.

## 2. Epoching

### Replication configuration

- epoch length: 30 s
- overlap: 15 s

Each epoch must retain `subject_id`, `diagnosis`, and an `epoch_id`.

Epochs are repeated observations from the same participant and are **not independent subjects**.

## 3. DICE-style spectral replication

Use Welch power spectral density estimation and fixed frequency bands:

- delta: 0.5–4 Hz
- theta: 4–8 Hz
- alpha: 8–13 Hz
- beta: 13–25 Hz
- gamma: 25–45 Hz

Relative band power:

```text
RBP_band = band_power / total_power_0.5_45Hz
```

Compute per channel and summarize at the subject level for statistical analyses.

## 4. Spectral critique

### 4.1 Absolute power
Compute log absolute band power alongside relative power.

### 4.2 Individual Alpha Frequency
Estimate IAF where a valid posterior alpha peak is identifiable. Store an explicit validity flag rather than forcing an IAF estimate for every subject.

### 4.3 Individualized bands
Define subject-specific spectral bands relative to IAF according to a prespecified rule.

### 4.4 Periodic / aperiodic decomposition
Using `specparam`, estimate:

- aperiodic exponent
- aperiodic offset
- alpha peak frequency
- alpha peak amplitude above aperiodic background
- alpha bandwidth

The exact frequency range and fitting criteria must be fixed in `config.yaml` before the final run.

## 5. Connectivity replication and critique

### 5.1 Spectral coherence
Reproduce SCC as closely as possible to the reference implementation.

### 5.2 Alternative measures
Compute at least:

- weighted phase-lag index (wPLI)
- imaginary coherence

Optional:

- debiased wPLI

### 5.3 Reference sensitivity
Repeat the primary connectivity analysis using the dataset derivative reference and common-average reference.

## 6. Group comparisons

Primary contrasts:

- AD vs CN
- FTD vs CN
- AD vs FTD

For each feature report:

- group descriptive statistics
- effect size
- p-value
- FDR-adjusted p-value when multiple features/electrodes are tested

Do not interpret significance alone as evidence of biomarker quality.

## 7. MMSE analysis

Perform Spearman correlation between candidate biomarkers and MMSE.

Report:

1. all-subject analysis
2. AD + FTD only analysis

The clinical-only analysis is important because the control group may contain strong MMSE ceiling effects.

## 8. Confounder-aware analysis

For selected robust biomarkers fit subject-level regression models such as:

```text
biomarker ~ diagnosis + age + sex
```

The purpose is sensitivity analysis, not automatic causal adjustment.

## 9. Machine-learning feature families

Compare feature families using identical validation logic:

1. RBP
2. SCC
3. RBP + SCC
4. IAF + individualized spectral features
5. periodic + aperiodic spectral features
6. wPLI / imaginary coherence
7. final robust combined biomarker set

## 10. Models

Primary:

- logistic regression
- linear SVM

Secondary nonlinear comparison:

- XGBoost

Deep learning is outside the initial analysis plan.

## 11. Metrics

Report subject-level:

- balanced accuracy
- ROC-AUC
- sensitivity
- specificity
- F1
- MCC

Whenever feasible, report fold-wise distributions and uncertainty rather than only a single point estimate.

## 12. Minimal-electrode optimization

Perform channel selection inside training data only.

Candidate approaches:

- sequential forward selection
- backward elimination
- predefined clinically practical montages

Evaluate both:

1. classification performance preservation
2. robust biomarker preservation

The smallest acceptable montage should satisfy prespecified performance and biomarker-preservation tolerances.
