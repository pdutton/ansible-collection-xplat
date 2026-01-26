#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: tempfile
short_description: Creates temporary files and directories
description:
  - This module is a cross-platform wrapper that abstracts differences between
    ansible.builtin.tempfile (used on Linux and macOS) and ansible.windows.win_tempfile
    (used on Windows).
  - It provides a consistent interface for creating temporary files and directories
    across all platforms.
  - The actual implementation delegates to the appropriate platform-specific module.

options:
  state:
    description:
      - Whether to create a temporary file or directory.
    type: str
    choices: [directory, file]
    default: file

  path:
    description:
      - Location where temporary file or directory should be created.
      - If not specified, uses the default temp directory for the platform.
    type: path

  prefix:
    description:
      - Prefix for file/directory name.
    type: str
    default: ansible.

  suffix:
    description:
      - Suffix for file/directory name.
    type: str
    default: ""

author:
  - Paul Dutton (@pdutton)

notes:
  - This is an action plugin that delegates to platform-specific modules.
  - For Linux/macOS uses ansible.builtin.tempfile
  - For Windows uses ansible.windows.win_tempfile
  - The created file or directory is not automatically cleaned up.
'''

EXAMPLES = r'''
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

- name: Create temp file in specific location
  pdutton.xplat.tempfile:
    state: file
    path: /var/tmp
    prefix: data_
    suffix: .json

- name: Use the created temporary file
  pdutton.xplat.copy:
    content: "temporary data"
    dest: "{{ tempfile_result.path }}"
'''

RETURN = r'''
path:
  description: Path to the created temporary file or directory.
  type: str
  returned: success
  sample: /tmp/ansible.abc123.tmp
'''
