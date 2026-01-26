.PHONY: build install uninstall test clean help

COLLECTION_NAMESPACE := pdutton
COLLECTION_NAME := xplat
COLLECTION_VERSION := $(shell grep -E '^\s*version:' galaxy.yml | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
COLLECTION_ARTIFACT := $(COLLECTION_NAMESPACE)-$(COLLECTION_NAME)-$(COLLECTION_VERSION).tar.gz

help:
	@echo "Available targets:"
	@echo "  make build      - Build the collection artifact"
	@echo "  make install    - Install the collection locally"
	@echo "  make uninstall  - Remove the installed collection"
	@echo "  make test       - Run integration tests"
	@echo "  make clean      - Remove build artifacts"

build:
	@echo "Building collection artifact..."
	ansible-galaxy collection build

install: build
	@echo "Installing collection..."
	ansible-galaxy collection install $(COLLECTION_ARTIFACT) --force

uninstall:
	@echo "Uninstalling collection..."
	ansible-galaxy collection remove $(COLLECTION_NAMESPACE).$(COLLECTION_NAME)

test:
	@echo "Running integration tests..."
	ansible-playbook tests/test_stat.yml
	ansible-playbook tests/test_basename.yml
	ansible-playbook tests/test_dirname.yml
	ansible-playbook tests/test_splitext.yml
	ansible-playbook tests/test_join.yml

clean:
	@echo "Cleaning build artifacts..."
	rm -f $(COLLECTION_ARTIFACT)
	rm -f MANIFEST.json
	rm -rf __pycache__
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete
