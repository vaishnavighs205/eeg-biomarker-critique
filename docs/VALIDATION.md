# Validation and Leakage Prevention

## Core rule

**The participant is the independent statistical unit.**

A participant may generate many overlapping EEG windows, but windows from the same person cannot appear in both training and testing.

## Prohibited workflow

```text
all epochs
   |
random train/test split
   |
train model
```

This leaks participant-specific information.

## Correct workflow

```text
subjects
   |
outer train/test split
   |
TRAIN SUBJECTS ONLY
   |-- scaling
   |-- feature filtering
   |-- hyperparameter tuning
   `-- electrode selection
   |
locked pipeline
   |
OUTER TEST SUBJECTS
```

## Recommended final validation

Use nested subject-wise cross-validation.

### Outer loop

Evaluate generalization to unseen subjects.

Recommended starting configuration:

- 5-fold stratified subject-level CV
- grouping variable = subject ID

### Inner loop

Used only on outer-training subjects for:

- hyperparameter tuning
- feature selection
- channel selection
- model choice when prespecified

## Preprocessing leakage

Fit all learned transformations on training data only, including:

- standardization
- imputation
- dimensionality reduction
- feature selection
- channel ranking

## Epoch predictions

If models operate on epochs, aggregate epoch-level probabilities into one subject-level prediction before computing the headline metrics.

Example:

```text
P(AD | subject) = mean(P(AD | epoch_i))
```

Alternative aggregation rules must be prespecified.

## LOSO replication

Leave-One-Subject-Out may be used as a reference experiment when reproducing the original study, but the main final comparison should use a consistent nested subject-level framework for all feature families.

## Repeated observations and statistics

Do not run ordinary independent-sample statistical tests on thousands of overlapping windows and interpret the resulting p-values as if the sample size were thousands of people.

Prefer subject-level summaries or models that explicitly account for repeated observations.
