# Build
.PHONY = build
build: deps

# Deps
.PHONY = deps
deps:
	pip install -r requirements.txt

# Docker Build
.PHONY = docker/build
docker/build:
	docker build -t maruja .

# Docker Clear
.PHONY = docker/clear
docker/clear:
	docker rmi -f maruja

# Build
.PHONY = run
run:
	docker run maruja --output capture

# Test
.PHONY = test
test: deps
	python -m unittest discover -s ./tests/ -p '*_test.py'
