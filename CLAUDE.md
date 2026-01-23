# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**pdutton.xplat** is an Ansible collection providing cross-platform plugins that abstract differences between Linux, Windows, and macOS. It allows playbooks to use a single plugin that delegates to the appropriate Ansible module based on the target platform.

**Planned plugins:**
- `pdutton.xplat.copy` - abstracts `ansible.builtin.command` (Linux/Mac) vs `ansible.windows.win_copy`
- `pdutton.xplat.command` - abstracts `ansible.builtin.command` (Linux/Mac) vs `ansible.windows.win_command`
- `pdutton.xplat.file` - abstracts `ansible.builtin.file` (Linux/Mac) vs `ansible.windows.win_file`
- `pdutton.xplat.stat` - abstracts `ansible.builtin.stat` (Linux/Mac) vs `ansible.windows.win_stat`

This project is in early development (initial commit). The directory structure and core plugins have not yet been implemented.

## Ansible Collection Structure

When implementing this collection, follow the standard Ansible collection layout:

```
plugins/
  modules/           # Custom module implementations
  action/            # Action plugins to handle task execution
roles/               # Reusable roles
tests/               # Test playbooks and test suites
galaxy.yml           # Collection metadata (namespace, name, version)
README.md            # User-facing documentation
MANIFEST.json        # Auto-generated manifest file
```

Key files to create:
- `galaxy.yml` - Defines collection metadata (namespace: `pdutton`, name: `xplat`)
- Plugin files in `plugins/modules/` or `plugins/action/` directories
- Test playbooks in `tests/` directory

## Development Commands

Once plugins are implemented, common development tasks will include:

**Testing the collection:**
```bash
# Run ansible-test (if integrated into test suite)
ansible-test integration
ansible-test sanity
ansible-test units

# Or manually test plugins in playbooks
ansible-playbook test_playbook.yml
```

**Installing the collection locally:**
```bash
# Build the collection
ansible-galaxy collection build

# Install from built artifact
ansible-galaxy collection install pdutton-xplat-*.tar.gz
```

**Validating syntax and structure:**
```bash
ansible-playbook --syntax-check <playbook>
```

## Key Architecture Decisions

**Plugin Abstraction Strategy:**
- Plugins should inspect the target platform (`ansible_os_family` or `ansible_system`) at runtime
- Delegate to the appropriate module based on the detected OS
- Ensure argument passthrough is compatible with both Unix and Windows variants
- Document parameter compatibility differences between platforms

**Module Selection Logic:**
Currently planning simple OS detection:
- Linux/Mac: use `ansible.builtin.*` modules
- Windows: use `ansible.windows.*` modules

Consider using action plugins or module_utils wrappers to handle platform detection and delegation cleanly.

## Documentation

- See README.md for user-facing feature overview
- Update README.md with usage examples once plugins are implemented
- Add inline comments in plugins explaining platform-specific behavior

## Git Workflow

Follow the instructions in the global ~/.claude/CLAUDE.md:
- Create a branch for new features or changes
- Commit changes with clear messages
