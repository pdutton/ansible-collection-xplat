#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: stat
short_description: Retrieve file or file system status
description:
  - This module is a cross-platform wrapper that abstracts differences between
    ansible.builtin.stat (used on Linux and macOS) and ansible.windows.win_stat
    (used on Windows).
  - It provides a consistent interface for retrieving file and filesystem
    information across all platforms.
  - The actual implementation delegates to the appropriate platform-specific module.

options:
  path:
    description:
      - The full path of the file/object to get the facts of.
    type: path
    required: true
    aliases: [ dest, name ]

  checksum_algorithm:
    description:
      - Algorithm to determine checksum of file.
      - Will throw an error if the host is unable to use specified algorithm.
      - On RHEL 6, the C(sha256) algorithm is only available if python-hashlib is installed.
      - Linux distributions have varying default support for these, but all
        support C(sha1) and C(md5).
    type: str
    choices: [ md5, sha1, sha224, sha256, sha384, sha512 ]
    default: sha1

  follow:
    description:
      - Whether to follow symlinks.
    type: bool
    default: true

  get_checksum:
    description:
      - Whether to return a checksum of the file.
    type: bool
    default: true

author:
  - Paul Dutton (@pdutton)

notes:
  - This is an action plugin that delegates to platform-specific modules.
  - For Linux/macOS: Uses ansible.builtin.stat
  - For Windows: Uses ansible.windows.win_stat
'''

EXAMPLES = r'''
- name: Stat a file
  pdutton.xplat.stat:
    path: /etc/hostname
  register: result

- name: Show file information
  debug:
    msg: "File exists: {{ result.stat.exists }}, Size: {{ result.stat.size }}"
'''

RETURN = r'''
stat:
  description:
    - Attributes of the remote file, including checksum, permissions, ownership,
      etc.
    - This data structure is exactly the same as ansible.builtin.stat with the
      addition of filesystem attributes.
  type: dict
  returned: all
  contains:
    exists:
      description: Whether the file exists
      type: bool
      returned: always
    isdir:
      description: Whether the path is a directory
      type: bool
      returned: always
    isfile:
      description: Whether the path is a regular file
      type: bool
      returned: always
    size:
      description: Size of the file in bytes
      type: int
      returned: when exists is true
    path:
      description: The full path that was checked
      type: str
      returned: always
    checksum:
      description: The checksum of the file
      type: str
      returned: when checksum_algorithm is specified and file exists
'''
