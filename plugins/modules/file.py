#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: file
short_description: Manage files and file properties
description:
  - This module is a cross-platform wrapper that abstracts differences between
    ansible.builtin.file (used on Linux and macOS) and ansible.windows.win_file
    (used on Windows).
  - It provides a consistent interface for managing files and directories across
    all platforms.
  - The actual implementation delegates to the appropriate platform-specific module.

options:
  path:
    description:
      - Path to the file being managed.
    type: path
    required: true
    aliases: [ dest, name ]

  state:
    description:
      - If C(absent), directories will be recursively deleted, and files or
        symlinks will be unlinked.
      - If C(directory), all intermediate subdirectories will be created if
        they do not exist.
      - If C(file), with other options, the file will be modified.
      - If C(hard), the hard link will be created or changed.
      - If C(link), the symbolic link will be created or changed.
      - If C(touch), an empty file will be created if it does not exist.
    type: str
    choices: [ absent, directory, file, hard, link, touch ]
    default: file

  src:
    description:
      - Path of the file to link to.
      - Required when I(state=link) or I(state=hard).
    type: path

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

  recurse:
    description:
      - Recursively set the specified file attributes on directory contents.
      - Only applies when I(state=directory).
    type: bool
    default: false

  force:
    description:
      - Force the creation of symlinks in two cases.
      - The source file does not exist (but will appear later).
      - The destination exists and is a file (replaces it with the link).
    type: bool
    default: false

  follow:
    description:
      - This flag indicates that filesystem links, if they exist, should be followed.
    type: bool
    default: true

author:
  - Paul Dutton (@pdutton)

notes:
  - This is an action plugin that delegates to platform-specific modules.
  - For Linux/macOS uses ansible.builtin.file
  - For Windows uses ansible.windows.win_file
  - Some parameters like mode, owner, group, and symlinks only apply to Unix systems.
'''

EXAMPLES = r'''
- name: Create a directory if it does not exist
  pdutton.xplat.file:
    path: /etc/myapp
    state: directory
    mode: '0755'

- name: Remove a file if it exists
  pdutton.xplat.file:
    path: /etc/myapp/old.conf
    state: absent

- name: Create a symbolic link
  pdutton.xplat.file:
    src: /etc/myapp/current.conf
    path: /etc/myapp/myapp.conf
    state: link

- name: Touch a file (create if not exists, update mtime if exists)
  pdutton.xplat.file:
    path: /tmp/myfile.txt
    state: touch
    mode: '0644'

- name: Change file ownership and permissions
  pdutton.xplat.file:
    path: /etc/myapp/config.yml
    owner: myuser
    group: mygroup
    mode: '0600'
'''

RETURN = r'''
dest:
  description: Destination file/path.
  type: str
  returned: success
  sample: /etc/foo.conf
path:
  description: Destination file/path, same as dest.
  type: str
  returned: success
  sample: /etc/foo.conf
state:
  description: State of the target.
  type: str
  returned: success
  sample: directory
mode:
  description: Permissions of the target, after execution.
  type: str
  returned: success (Unix only)
  sample: "0755"
owner:
  description: Owner of the file, after execution.
  type: str
  returned: success (Unix only)
  sample: root
group:
  description: Group of the file, after execution.
  type: str
  returned: success (Unix only)
  sample: root
size:
  description: Size of the file, after execution.
  type: int
  returned: success
  sample: 1024
'''
