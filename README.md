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

### Using pdutton.xplat.find

The `find` plugin returns a list of files based on specific criteria:

```yaml
- name: Find all .log files in /var/log
  pdutton.xplat.find:
    paths: /var/log
    patterns: '*.log'

- name: Find files older than 1 week
  pdutton.xplat.find:
    paths: /tmp
    age: 1w
    recurse: yes

- name: Find files larger than 1MB
  pdutton.xplat.find:
    paths: /home
    size: 1m
    recurse: yes
```

The plugin automatically detects the target platform and delegates to:
- `ansible.builtin.find` on Linux and macOS
- `ansible.windows.win_find` on Windows

### Using pdutton.xplat.get_url

The `get_url` plugin downloads files from HTTP, HTTPS, or FTP:

```yaml
- name: Download a file
  pdutton.xplat.get_url:
    url: https://example.com/file.tar.gz
    dest: /tmp/file.tar.gz

- name: Download with checksum validation
  pdutton.xplat.get_url:
    url: https://example.com/file.zip
    dest: /tmp/file.zip
    checksum: sha256:abc123def456...

- name: Download with authentication
  pdutton.xplat.get_url:
    url: https://secure.example.com/file.bin
    dest: /opt/files/file.bin
    url_username: myuser
    url_password: mypassword
```

The plugin automatically detects the target platform and delegates to:
- `ansible.builtin.get_url` on Linux and macOS
- `ansible.windows.win_get_url` on Windows

### Using pdutton.xplat.group

The `group` plugin manages groups:

```yaml
- name: Create a group
  pdutton.xplat.group:
    name: developers
    state: present

- name: Remove a group
  pdutton.xplat.group:
    name: developers
    state: absent

- name: Create a group with specific GID (Unix)
  pdutton.xplat.group:
    name: developers
    gid: 1500
```

The plugin automatically detects the target platform and delegates to:
- `ansible.builtin.group` on Linux and macOS
- `ansible.windows.win_group` on Windows

### Using pdutton.xplat.hostname

The `hostname` plugin manages the system hostname:

```yaml
- name: Set the hostname
  pdutton.xplat.hostname:
    name: myserver.example.com

- name: Set hostname using specific strategy (Unix)
  pdutton.xplat.hostname:
    name: myserver
    use: systemd
```

The plugin automatically detects the target platform and delegates to:
- `ansible.builtin.hostname` on Linux and macOS
- `ansible.windows.win_hostname` on Windows

### Using pdutton.xplat.lineinfile

The `lineinfile` plugin manages lines in text files:

```yaml
- name: Ensure a line is present in a file
  pdutton.xplat.lineinfile:
    path: /etc/hosts
    line: 192.168.1.99 myhost.example.com

- name: Replace a line using regex
  pdutton.xplat.lineinfile:
    path: /etc/selinux/config
    regexp: '^SELINUX='
    line: SELINUX=enforcing

- name: Remove a line from a file
  pdutton.xplat.lineinfile:
    path: /etc/sudoers
    state: absent
    regexp: '^%wheel'
```

The plugin automatically detects the target platform and delegates to:
- `ansible.builtin.lineinfile` on Linux and macOS
- `ansible.windows.win_lineinfile` on Windows

### Using pdutton.xplat.ping

The `ping` plugin tests connectivity (not ICMP ping, but Ansible connectivity):

```yaml
- name: Test connectivity
  pdutton.xplat.ping:

- name: Test connectivity with custom return data
  pdutton.xplat.ping:
    data: hello
  register: result

- name: Debug ping result
  ansible.builtin.debug:
    var: result.ping
```

The plugin automatically detects the target platform and delegates to:
- `ansible.builtin.ping` on Linux and macOS
- `ansible.windows.win_ping` on Windows

### Using pdutton.xplat.reboot

The `reboot` plugin reboots machines and waits for them to come back online:

```yaml
- name: Reboot the machine
  pdutton.xplat.reboot:

- name: Reboot with a longer timeout
  pdutton.xplat.reboot:
    reboot_timeout: 900

- name: Reboot with delay
  pdutton.xplat.reboot:
    pre_reboot_delay: 30
    post_reboot_delay: 60
```

The plugin automatically detects the target platform and delegates to:
- `ansible.builtin.reboot` on Linux and macOS
- `ansible.windows.win_reboot` on Windows

### Using pdutton.xplat.service

The `service` plugin manages services:

```yaml
- name: Start a service
  pdutton.xplat.service:
    name: httpd
    state: started

- name: Stop a service
  pdutton.xplat.service:
    name: httpd
    state: stopped

- name: Start and enable a service
  pdutton.xplat.service:
    name: httpd
    state: started
    enabled: yes
```

The plugin automatically detects the target platform and delegates to:
- `ansible.builtin.service` on Linux and macOS
- `ansible.windows.win_service` on Windows

### Using pdutton.xplat.shell

The `shell` plugin executes shell commands (with shell features like pipes and redirects):

```yaml
- name: Run a shell command
  pdutton.xplat.shell:
    cmd: echo $HOME
  register: result

- name: Run a shell command with pipes
  pdutton.xplat.shell:
    cmd: cat /etc/passwd | grep root

- name: Run command in specific directory
  pdutton.xplat.shell:
    cmd: ls -la | wc -l
    chdir: /tmp
```

The plugin automatically detects the target platform and delegates to:
- `ansible.builtin.shell` on Linux and macOS
- `ansible.windows.win_shell` on Windows

### Using pdutton.xplat.tempfile

The `tempfile` plugin creates temporary files and directories:

```yaml
- name: Create a temporary file
  pdutton.xplat.tempfile:
    state: file
    suffix: .tmp
  register: tempfile_result

- name: Create a temporary directory
  pdutton.xplat.tempfile:
    state: directory
    prefix: myapp_
  register: tempdir_result

- name: Use the created temporary file
  pdutton.xplat.copy:
    content: "temporary data"
    dest: "{{ tempfile_result.path }}"
```

The plugin automatically detects the target platform and delegates to:
- `ansible.builtin.tempfile` on Linux and macOS
- `ansible.windows.win_tempfile` on Windows

### Using pdutton.xplat.template

The `template` plugin templates files using Jinja2:

```yaml
- name: Template a file to the remote machine
  pdutton.xplat.template:
    src: templates/myconfig.j2
    dest: /etc/myapp/config.conf
    owner: root
    group: root
    mode: '0644'

- name: Template with backup
  pdutton.xplat.template:
    src: templates/app.conf.j2
    dest: /opt/app/app.conf
    backup: yes
```

The plugin automatically detects the target platform and delegates to:
- `ansible.builtin.template` on Linux and macOS
- `ansible.windows.win_template` on Windows

### Using pdutton.xplat.uri

The `uri` plugin interacts with webservices:

```yaml
- name: Make a GET request
  pdutton.xplat.uri:
    url: https://api.example.com/data
  register: result

- name: Make a POST request with JSON body
  pdutton.xplat.uri:
    url: https://api.example.com/data
    method: POST
    body:
      name: test
      value: 123
    body_format: json

- name: Download a file
  pdutton.xplat.uri:
    url: https://example.com/file.zip
    dest: /tmp/file.zip
```

The plugin automatically detects the target platform and delegates to:
- `ansible.builtin.uri` on Linux and macOS
- `ansible.windows.win_uri` on Windows

### Using pdutton.xplat.user

The `user` plugin manages user accounts:

```yaml
- name: Create a user
  pdutton.xplat.user:
    name: johnd
    comment: John Doe
    state: present

- name: Remove a user
  pdutton.xplat.user:
    name: johnd
    state: absent

- name: Create user with specific groups
  pdutton.xplat.user:
    name: johnd
    groups:
      - wheel
      - developers
    append: yes
```

The plugin automatically detects the target platform and delegates to:
- `ansible.builtin.user` on Linux and macOS
- `ansible.windows.win_user` on Windows

### Using pdutton.xplat.wait_for

The `wait_for` plugin waits for a condition before continuing:

```yaml
- name: Wait for port 8080 to be open
  pdutton.xplat.wait_for:
    port: 8080
    state: started

- name: Wait for file to exist
  pdutton.xplat.wait_for:
    path: /tmp/ready.txt

- name: Wait for file to contain specific text
  pdutton.xplat.wait_for:
    path: /var/log/app.log
    search_regex: "Application started"

- name: Wait with custom timeout
  pdutton.xplat.wait_for:
    port: 3306
    timeout: 600
    delay: 10
```

The plugin automatically detects the target platform and delegates to:
- `ansible.builtin.wait_for` on Linux and macOS
- `ansible.windows.win_wait_for` on Windows
