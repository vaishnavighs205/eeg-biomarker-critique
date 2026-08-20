# Biomarker Critique Framework

A candidate EEG biomarker is not considered robust simply because it yields a low p-value or improves classification.

## Criterion 1 — Reproducibility
Can the feature reproduce the expected AD vs CN effect in a faithful DICE-style pipeline?

## Criterion 2 — Spectral definition stability
Does the effect survive:

- fixed vs individualized frequency bands?
- relative vs absolute power?
- periodic vs aperiodic separation?

## Criterion 3 — Connectivity-method stability
Does a connectivity effect survive replacement of ordinary coherence with wPLI or imaginary coherence?

## Criterion 4 — Reference stability
Does the result remain qualitatively similar after a reasonable rereferencing sensitivity analysis?

## Criterion 5 — Disease specificity
Does the biomarker distinguish:

- AD from CN?
- FTD from CN?
- AD from FTD?

Possible interpretations:

- AD-specific candidate
- general dementia/neurodegeneration marker
- nonspecific group difference

## Criterion 6 — Cognitive relevance
Does the biomarker associate with MMSE, particularly within AD + FTD rather than only across diagnostic groups?

## Criterion 7 — Incremental ML value
Does the feature family improve held-out subject-level performance when added to a strong baseline?

## Criterion 8 — Electrode robustness
Can the biomarker be estimated reliably using a sparse electrode montage?

## Final biomarker status

Suggested labels:

- **Robust** — survives most prespecified tests and contributes interpretable information
- **Conditional** — useful under specific methodological assumptions
- **Weak** — unstable, nonspecific or adds little independent value
- **Unsupported** — fails reproduction or becomes uninterpretable under sensitivity analyses

These labels should be assigned from predefined criteria, not retrofitted after seeing the results.
