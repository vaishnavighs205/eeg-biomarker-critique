# Contributing

## Development rules

1. Keep reusable logic in `src/eeg_biomarkers/`, not only in notebooks.
2. Do not commit EEG recordings or participant-level exports containing unnecessary sensitive metadata.
3. Every feature table must retain `subject_id`.
4. Any learned preprocessing, feature selection or channel selection must be fitted inside training folds only.
5. Add methodological decisions to `docs/DECISION_LOG.md`.
6. Prefer small, testable functions over monolithic notebooks.
7. Add or update tests for reusable analysis utilities.

## Branch naming

Examples:

```text
feature/qc-loader
feature/rbp-replication
feature/specparam
feature/connectivity-wpli
analysis/ml-comparison
analysis/channel-selection
fix/subject-leakage
```
