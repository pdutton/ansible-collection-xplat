#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: copy
short_description: Copy files to remote locations
description:
  - This module is a cross-platform wrapper that abstracts differences between
    ansible.builtin.copy (used on Linux and macOS) and ansible.windows.win_copy
    (used on Windows).
  - It provides a consistent interface for copying files to remote hosts across
    all platforms.
  - The actual implementation delegates to the appropriate platform-specific module.

options:
  src:
    description:
      - Local path to a file to copy to the remote server.
      - This can be absolute or relative.
      - If path is a directory, it is copied recursively.
      - Mutually exclusive with I(content).
    type: path

  content:
    description:
      - When used instead of I(src), sets the contents of a file directly to
        the specified value.
      - Mutually exclusive with I(src).
    type: str

  dest:
    description:
      - Remote absolute path where the file should be copied to.
    type: path
    required: true

  backup:
    description:
      - Create a backup file including the timestamp information.
    type: bool
    default: false

  force:
    description:
      - If C(true), will replace the remote file when contents are different.
      - If C(false), the file will only be transferred if the destination does
        not exist.
    type: bool
    default: true

  mode:
    description:
      - The permissions of the destination file or directory.
      - For Unix systems, use octal numbers (e.g., C(0644)) or symbolic mode.
      - For Windows, this parameter is ignored.
    type: raw

  owner:
    description:
      - Name of the user that should own the file/directory on Unix systems.
      - For Windows, this parameter is ignored.
    type: str

  group:
    description:
      - Name of the group that should own the file/directory on Unix systems.
      - For Windows, this parameter is ignored.
    type: str

  remote_src:
    description:
      - If C(true), go to the remote/target machine for the src.
    type: bool
    default: false

author:
  - Paul Dutton (@pdutton)

notes:
  - This is an action plugin that delegates to platform-specific modules.
  - For Linux/macOS uses ansible.builtin.copy
  - For Windows uses ansible.windows.win_copy
  - Some parameters like mode, owner, and group only apply to Unix systems.
'''

EXAMPLES = r'''
- name: Copy file with owner and permissions
  pdutton.xplat.copy:
    src: /srv/myfiles/foo.conf
    dest: /etc/foo.conf
    owner: root
    group: root
    mode: '0644'

- name: Copy file to remote with content
  pdutton.xplat.copy:
    content: "Hello World\n"
    dest: /tmp/hello.txt

- name: Copy a directory
  pdutton.xplat.copy:
    src: /srv/myapp/
    dest: /opt/myapp/
'''

RETURN = r'''
dest:
  description: Destination file/path.
  type: str
  returned: success
  sample: /etc/foo.conf
src:
  description: Source file used for the copy.
  type: str
  returned: changed
  sample: /home/user/foo.conf
checksum:
  description: SHA1 checksum of the file after running copy.
  type: str
  returned: success
  sample: 6e642bb8dd5c2e027bf21dd923337cbb4214f827
size:
  description: Size of the target file after running copy.
  type: int
  returned: success
  sample: 1220
backup_file:
  description: Name of the backup file created when backup=yes.
  type: str
  returned: changed and backup=yes
  sample: /etc/foo.conf.2023-04-13@10:25:28~
'''
