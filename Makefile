# Build
.PHONY = build
build: deps

# Virtual Environment
.PHONY = venv
venv:
	python -m venv .venv
	source .venv/bin/activate

# Deps
.PHONY = deps
deps: venv
	pip install -r requirements.txt

# Docker Build
.PHONY = docker/build
docker/build:
	docker build -t maruja .

# Build
.PHONY = run
run:
	docker run maruja --output capture

# Test
.PHONY = test
test: deps
	python -m unittest discover -s ./tests/ -p '*_test.py'