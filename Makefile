.PHONY: build install uninstall test clean help

CollectionNamespace := pdutton
CollectionName := xplat
CollectionVersion := $(shell grep -E '^\s*version:' galaxy.yml | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
CollectionArtifact := $(CollectionNamespace)-$(CollectionName)-$(CollectionVersion).tar.gz

AnsibleCollectionsPath?=~/.ansible/collections/ansible_collections

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
	ansible-galaxy collection install $(CollectionArtifact) --force

uninstall:
	@echo "Uninstalling collection..."
	rm -rf $(AnsibleCollectionsPath)/$(CollectionNamespace)/$(CollectionName)

test:
	@echo "Running integration tests..."
	ansible-playbook tests/test_stat.yml
	ansible-playbook tests/test_basename.yml
	ansible-playbook tests/test_dirname.yml
	ansible-playbook tests/test_splitext.yml
	ansible-playbook tests/test_join.yml

clean:
	@echo "Cleaning build artifacts..."
	rm -f $(CollectionArtifact)
	rm -f MANIFEST.json
	rm -rf __pycache__
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete
