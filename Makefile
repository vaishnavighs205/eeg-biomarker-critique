.PHONY: install test qc

install:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest -q

qc:
	python scripts/run_qc.py --config config.yaml
