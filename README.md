# Ansible Collection: XPlat

The pdutton.xplat collection provides cross platform functionality Ansible.

## What is included

Initially this collection will provide cross platform plugins for basic tasks that require different modules
on different operating systems.

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

### Using pdutton.xplat.copy

The `copy` plugin copies files to remote locations across different platforms:

```yaml
- name: Copy file with content
  pdutton.xplat.copy:
    content: "Hello World\n"
    dest: /tmp/hello.txt

- name: Copy a local file to remote
  pdutton.xplat.copy:
    src: /local/path/myfile.conf
    dest: /etc/myapp/myfile.conf
    owner: root
    group: root
    mode: '0644'
```

The plugin automatically detects the target platform and delegates to:
- `ansible.builtin.copy` on Linux and macOS
- `ansible.windows.win_copy` on Windows

### Using pdutton.xplat.command

The `command` plugin executes commands on targets across different platforms:

```yaml
- name: Run a simple command
  pdutton.xplat.command:
    cmd: whoami
  register: result

- name: Run command with arguments as list
  pdutton.xplat.command:
    argv:
      - /usr/bin/python3
      - --version

- name: Run command only if file does not exist
  pdutton.xplat.command:
    cmd: touch /tmp/myfile
    creates: /tmp/myfile
```

The plugin automatically detects the target platform and delegates to:
- `ansible.builtin.command` on Linux and macOS
- `ansible.windows.win_command` on Windows

### Using pdutton.xplat.file

The `file` plugin manages files and file properties across different platforms:

```yaml
- name: Create a directory
  pdutton.xplat.file:
    path: /etc/myapp
    state: directory
    mode: '0755'

- name: Touch a file
  pdutton.xplat.file:
    path: /tmp/myfile.txt
    state: touch

- name: Remove a file
  pdutton.xplat.file:
    path: /tmp/old_file.txt
    state: absent

- name: Create a symbolic link
  pdutton.xplat.file:
    src: /etc/myapp/current.conf
    path: /etc/myapp/myapp.conf
    state: link
```

The plugin automatically detects the target platform and delegates to:
- `ansible.builtin.file` on Linux and macOS
- `ansible.windows.win_file` on Windows
