# Ansible Collection: XPlat

The pdutton.xplat collection provides cross platform functionality Ansible.

## What is included

Initially this collecton will provide cross platform plugins for basic tasks that require different modules
on different operating sytems.

Included plugins:
    - pdutton.xplat.copy to call ansible.builtin.copy or ansible.windows.win_copy
    - pdutton.xplat.command to call ansible.builtin.command or ansible.windows.win_command
    - pdutton.xplat.file to call  ansible.builtin.file or ansible.windows.win_file
    - pdutton.xplat.stat to call  ansible.builtin.stat or ansible.windows.win_stat

## Platforms

Linux, Windows, and Mac will initially be supported.

## Installation

Install from a git repository using ansible-galaxy:

```bash
ansible-galaxy collection install git+https://github.com/pdutton/ansible-collection-xplat.git
```

For additional installation options, see the [Ansible documentation on installing collections from a git repository](https://docs.ansible.com/projects/ansible/latest/collections_guide/collections_installing.html#installing-a-collection-from-a-git-repository).

## Usage

### Using pdutton.xplat.stat

The `stat` plugin retrieves file or filesystem status information across different platforms:

```yaml
- name: Get file stats
  pdutton.xplat.stat:
    path: /etc/hostname
  register: file_stats

- name: Display file information
  debug:
    msg: |
      File: {{ file_stats.stat.path }}
      Exists: {{ file_stats.stat.exists }}
      Size: {{ file_stats.stat.size }} bytes
      Type: {{ 'directory' if file_stats.stat.isdir else 'file' if file_stats.stat.isfile else 'other' }}
```

The plugin automatically detects the target platform and delegates to:
- `ansible.builtin.stat` on Linux and macOS
- `ansible.windows.win_stat` on Windows

All parameters supported by the underlying modules are passed through transparently.
