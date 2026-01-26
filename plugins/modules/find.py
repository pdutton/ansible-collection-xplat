#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: find
short_description: Return a list of files based on specific criteria
description:
  - This module is a cross-platform wrapper that abstracts differences between
    ansible.builtin.find (used on Linux and macOS) and ansible.windows.win_find
    (used on Windows).
  - It provides a consistent interface for finding files across all platforms.
  - The actual implementation delegates to the appropriate platform-specific module.
  - Returns a list of files matching the specified criteria.

options:
  paths:
    description:
      - List of paths to search for files or directories.
    type: list
    elements: path
    required: true
    aliases: [name, path]

  patterns:
    description:
      - One or more shell or regex patterns for filenames to match.
      - Items matching any pattern will be included in the result.
    type: list
    elements: str
    default: ['*']

  excludes:
    description:
      - One or more patterns to exclude from the results.
    type: list
    elements: str

  use_regex:
    description:
      - If C(true), patterns are interpreted as Python regexes.
      - Otherwise, they are shell-style globs.
    type: bool
    default: false

  file_type:
    description:
      - Type of file to search for.
    type: str
    choices: [any, directory, file, link]
    default: file

  recurse:
    description:
      - If C(true), search recursively into subdirectories.
    type: bool
    default: false

  depth:
    description:
      - Maximum depth of search.
    type: int

  hidden:
    description:
      - Include hidden files in results.
    type: bool
    default: false

  follow:
    description:
      - Follow symbolic links.
    type: bool
    default: false

  age:
    description:
      - Select files whose age matches the time specified.
      - Use a negative age to find files equal to or older.
      - Use a positive age to find files equal to or newer.
    type: str

  age_stamp:
    description:
      - Choose the file property against which to compare age.
    type: str
    choices: [atime, ctime, mtime]
    default: mtime

  size:
    description:
      - Select files whose size matches the specified size.
      - Supports suffixes like b, k, m, g.
    type: str

  get_checksum:
    description:
      - Include a checksum of the file in the result.
    type: bool
    default: false

  checksum_algorithm:
    description:
      - Algorithm to use when generating checksums.
    type: str
    choices: [md5, sha1, sha224, sha256, sha384, sha512]
    default: sha1

author:
  - Paul Dutton (@pdutton)

notes:
  - This is an action plugin that delegates to platform-specific modules.
  - For Linux/macOS uses ansible.builtin.find
  - For Windows uses ansible.windows.win_find
'''

EXAMPLES = r'''
- name: Find all .log files in /var/log
  pdutton.xplat.find:
    paths: /var/log
    patterns: '*.log'

- name: Find all files older than 1 week
  pdutton.xplat.find:
    paths: /tmp
    age: 1w
    recurse: yes

- name: Find files larger than 1MB
  pdutton.xplat.find:
    paths: /home
    size: 1m
    recurse: yes

- name: Find directories only
  pdutton.xplat.find:
    paths: /opt
    file_type: directory
    recurse: yes

- name: Find files with checksum
  pdutton.xplat.find:
    paths: /etc
    patterns: '*.conf'
    get_checksum: yes
'''

RETURN = r'''
files:
  description: List of files matching the criteria.
  type: list
  returned: always
  elements: dict
  sample:
    - path: /var/log/syslog
      mode: "0644"
      isdir: false
      size: 12345
      mtime: 1680000000
matched:
  description: Number of files matched.
  type: int
  returned: always
  sample: 5
examined:
  description: Number of files examined.
  type: int
  returned: always
  sample: 100
'''
