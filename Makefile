##
## EPITECH PROJECT, 2024
## Makefile
## File description:
## Makefile
##

BINARY=pbrain-gomoku-ai
SOURCE=gomoku/brain.py

.PHONY: all build run test clean install

all: build

build: $(BINARY)

$(BINARY): $(SOURCE)
	@echo "Building binary: $(BINARY)"
	@echo '#!/usr/bin/env python3' > $(BINARY)
	@cat $(SOURCE) >> $(BINARY)
	@chmod +x $(BINARY)
	@echo "Binary $(BINARY) created."

run: build
	@echo "Running game..."
	@PYTHONPATH=$(shell pwd) ./$(BINARY)

test:
	@python3 -m unittest discover -s tests -p "*.py"

clean:
	@echo "Cleaning up..."
	@rm -f $(BINARY)
	@find . -name "*.pyc" -exec rm -f {} +
	@find . -name "__pycache__" -exec rm -rf {} +

install:
	@pip install -r requirements.txt

