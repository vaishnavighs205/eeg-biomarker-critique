#!/usr/bin/env bash
set -euo pipefail

SOURCE="https://github.com/OpenNeuroDatasets/ds004504.git"
TARGET="${1:-data/ds004504}"

if ! command -v datalad >/dev/null 2>&1; then
  echo "DataLad is required to retrieve git-annex EEG content."
  echo "Install it first, for example:"
  echo "  conda install -c conda-forge datalad git-annex"
  exit 1
fi

if [[ ! -d "$TARGET/.git" ]]; then
  echo "Installing ds004504 into $TARGET"
  datalad install -s "$SOURCE" "$TARGET"
else
  echo "Dataset already installed at $TARGET"
fi

pushd "$TARGET" >/dev/null

# Lightweight metadata needed by the pipeline.
datalad get participants.tsv participants.json dataset_description.json README || true

# The project starts from the authors' denoised derivative EEG.
# -r recursively retrieves the annexed .set recordings under derivatives/.
datalad get -r derivatives

popd >/dev/null

echo "Dataset ready at: $TARGET"
echo "Next: python scripts/run_qc.py --config config.yaml"
