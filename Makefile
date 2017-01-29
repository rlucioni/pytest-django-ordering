.PHONY: quality requirements

quality:
	flake8 .

requirements:
	pip install -U pip
	pip install -r requirements.txt
