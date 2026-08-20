# Decision Log

Use this file to record methodological decisions **before** looking at final results.

| Date | Decision | Rationale | Affects |
|---|---|---|---|
| YYYY-MM-DD | Example: use 30 s windows with 15 s overlap for replication | Match DICE-style setup | Replication |
| YYYY-MM-DD | Example: subject is independent unit | Prevent leakage/pseudoreplication | Statistics + ML |

## Decisions that must eventually be locked

- exact derivative files used
- exact preprocessing/reference for replication
- Welch PSD parameters
- IAF detection rule
- individualized-band definitions
- specparam frequency range and fit criteria
- connectivity frequency bands
- subject-level feature aggregation
- outer/inner CV split policy
- hyperparameter search spaces
- electrode-preservation thresholds
- exclusion criteria
