# Ansible Collection: XPlat

The pdutton.xplat collection provides cross platform functionality Ansible.

## What is included

Initially this collection will provide cross platform plugins for basic tasks that require different modules
on different operating systems.

Included plugins:
- `pdutton.xplat.command` - execute commands (`ansible.builtin.command` / `ansible.windows.win_command`)
- `pdutton.xplat.copy` - copy files (`ansible.builtin.copy` / `ansible.windows.win_copy`)
- `pdutton.xplat.file` - manage files and directories (`ansible.builtin.file` / `ansible.windows.win_file`)
- `pdutton.xplat.find` - find files based on criteria (`ansible.builtin.find` / `ansible.windows.win_find`)
- `pdutton.xplat.get_url` - download files from HTTP/HTTPS/FTP (`ansible.builtin.get_url` / `ansible.windows.win_get_url`)
- `pdutton.xplat.group` - manage groups (`ansible.builtin.group` / `ansible.windows.win_group`)
- `pdutton.xplat.hostname` - manage hostname (`ansible.builtin.hostname` / `ansible.windows.win_hostname`)
- `pdutton.xplat.lineinfile` - manage lines in text files (`ansible.builtin.lineinfile` / `ansible.windows.win_lineinfile`)
- `pdutton.xplat.ping` - test connectivity (`ansible.builtin.ping` / `ansible.windows.win_ping`)
- `pdutton.xplat.reboot` - reboot machines (`ansible.builtin.reboot` / `ansible.windows.win_reboot`)
- `pdutton.xplat.service` - manage services (`ansible.builtin.service` / `ansible.windows.win_service`)
- `pdutton.xplat.shell` - execute shell commands (`ansible.builtin.shell` / `ansible.windows.win_shell`)
- `pdutton.xplat.stat` - get file status (`ansible.builtin.stat` / `ansible.windows.win_stat`)
- `pdutton.xplat.tempfile` - create temporary files/directories (`ansible.builtin.tempfile` / `ansible.windows.win_tempfile`)
- `pdutton.xplat.template` - template files with Jinja2 (`ansible.builtin.template` / `ansible.windows.win_template`)
- `pdutton.xplat.uri` - interact with webservices (`ansible.builtin.uri` / `ansible.windows.win_uri`)
- `pdutton.xplat.user` - manage user accounts (`ansible.builtin.user` / `ansible.windows.win_user`)
- `pdutton.xplat.wait_for` - wait for conditions (`ansible.builtin.wait_for` / `ansible.windows.win_wait_for`)

Included filters (cross-platform path manipulation):
    - pdutton.xplat.basename - extract path basename from Unix or Windows paths
    - pdutton.xplat.dirname - extract directory name from Unix or Windows paths
    - pdutton.xplat.splitext - split path into root and extension
    - pdutton.xplat.join - join path components using appropriate separator

## Platforms

Linux, Windows, and Mac will initially be supported.

## Installation

Install from a git repository using ansible-galaxy:

```bash
ansible-galaxy collection install git+https://github.com/pdutton/ansible-collection-xplat.git --force
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

### Using pdutton.xplat.basename

The `basename` filter extracts the final component of a path string, automatically handling both Unix and Windows path formats:

```yaml
- name: Extract basename from a Unix path
  debug:
    msg: "{{ '/etc/hostname' | pdutton.xplat.basename }}"
  # Output: hostname

- name: Extract basename from a Windows path
  debug:
    msg: "{{ 'C:\\Windows\\System32\\cmd.exe' | pdutton.xplat.basename }}"
  # Output: cmd.exe

- name: Extract basename from a UNC path
  debug:
    msg: "{{ '\\\\server\\share\\file.txt' | pdutton.xplat.basename }}"
  # Output: file.txt
```

The filter automatically detects whether the input is a Unix-style or Windows-style path and applies the appropriate basename logic. This makes it useful for processing paths from different sources or when working with cross-platform variables.

### Using pdutton.xplat.dirname

The `dirname` filter extracts the directory portion of a path string:

```yaml
- name: Extract dirname from a Unix path
  debug:
    msg: "{{ '/etc/hostname' | pdutton.xplat.dirname }}"
  # Output: /etc

- name: Extract dirname from a Windows path
  debug:
    msg: "{{ 'C:\\Windows\\System32\\cmd.exe' | pdutton.xplat.dirname }}"
  # Output: C:\Windows\System32

- name: Extract dirname from a UNC path
  debug:
    msg: "{{ '\\\\server\\share\\folder\\file.txt' | pdutton.xplat.dirname }}"
  # Output: \\server\share\folder
```

### Using pdutton.xplat.splitext

The `splitext` filter splits a path into root and extension components, returning a list:

```yaml
- name: Split path into root and extension
  set_fact:
    path_parts: "{{ '/var/log/syslog.log' | pdutton.xplat.splitext }}"
- debug:
    msg: "Root: {{ path_parts[0] }}, Extension: {{ path_parts[1] }}"
  # Output: Root: /var/log/syslog, Extension: .log

- name: Split Windows path
  debug:
    msg: "{{ 'C:\\Windows\\System32\\cmd.exe' | pdutton.xplat.splitext }}"
  # Output: ['C:\Windows\System32\cmd', '.exe']

- name: Hidden files are handled correctly
  debug:
    msg: "{{ '/home/user/.bashrc' | pdutton.xplat.splitext }}"
  # Output: ['/home/user/.bashrc', ''] (no extension)
```

### Using pdutton.xplat.join

The `join` filter combines path components using the appropriate separator:

```yaml
- name: Join Unix path components
  debug:
    msg: "{{ '/home' | pdutton.xplat.join('user', 'documents', 'file.txt') }}"
  # Output: /home/user/documents/file.txt

- name: Join Windows path components
  debug:
    msg: "{{ 'C:\\Windows' | pdutton.xplat.join('System32', 'cmd.exe') }}"
  # Output: C:\Windows\System32\cmd.exe

- name: Build path from variables
  vars:
    base_dir: "/var/log"
    app_name: "myapp"
    log_file: "app.log"
  debug:
    msg: "{{ base_dir | pdutton.xplat.join(app_name, log_file) }}"
  # Output: /var/log/myapp/app.log
```

The path format (Unix or Windows) is determined by the base path (first argument).
