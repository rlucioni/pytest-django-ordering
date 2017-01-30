.PHONY: quality requirements test

quality:
	flake8 .

requirements:
	pip install -U pip
	pip install -r requirements.txt

test:
	pytest
