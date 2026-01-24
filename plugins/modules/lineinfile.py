#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: lineinfile
short_description: Manage lines in text files
description:
  - This module is a cross-platform wrapper that abstracts differences between
    ansible.builtin.lineinfile (used on Linux and macOS) and ansible.windows.win_lineinfile
    (used on Windows).
  - It provides a consistent interface for managing lines in files across all platforms.
  - The actual implementation delegates to the appropriate platform-specific module.
  - This module ensures a particular line is in a file, or replace an existing
    line using a back-referenced regular expression.

options:
  path:
    description:
      - The file to modify.
    type: path
    required: true
    aliases: [dest, destfile, name]

  line:
    description:
      - The line to insert/replace into the file.
      - Required for C(state=present).
    type: str

  regexp:
    description:
      - The regular expression to look for in every line of the file.
      - For C(state=present), the pattern to replace if found.
      - For C(state=absent), the pattern of the line(s) to remove.
    type: str

  state:
    description:
      - Whether the line should be present or absent.
    type: str
    choices: [absent, present]
    default: present

  backrefs:
    description:
      - If set, C(line) can contain backreferences (both positional and named).
      - Used with C(state=present) and C(regexp).
    type: bool
    default: false

  insertafter:
    description:
      - If specified, the line will be inserted after the last match of the
        specified regular expression.
      - A special value C(EOF) inserts at end of the file.
    type: str

  insertbefore:
    description:
      - If specified, the line will be inserted before the last match of the
        specified regular expression.
      - A special value C(BOF) inserts at beginning of the file.
    type: str

  create:
    description:
      - If specified and the file does not exist, a new file will be created.
    type: bool
    default: false

  backup:
    description:
      - Create a backup file including the timestamp information.
    type: bool
    default: false

  firstmatch:
    description:
      - When C(insertafter) or C(insertbefore) is used, the first match is used.
    type: bool
    default: false

  mode:
    description:
      - The permissions of the destination file.
      - For Unix systems only.
    type: raw

  owner:
    description:
      - Name of the user that should own the file.
      - For Unix systems only.
    type: str

  group:
    description:
      - Name of the group that should own the file.
      - For Unix systems only.
    type: str

  encoding:
    description:
      - Specifies the encoding of the source text file to operate on.
      - For Windows systems only.
    type: str
    default: auto

  newline:
    description:
      - Specifies the line separator style to use for the modified file.
      - For Windows systems only.
    type: str
    choices: [unix, windows]

author:
  - Paul Dutton (@pdutton)

notes:
  - This is an action plugin that delegates to platform-specific modules.
  - For Linux/macOS uses ansible.builtin.lineinfile
  - For Windows uses ansible.windows.win_lineinfile
  - Some parameters only apply to specific platforms as noted.
'''

EXAMPLES = r'''
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

- name: Insert a line after a pattern
  pdutton.xplat.lineinfile:
    path: /etc/httpd/conf/httpd.conf
    insertafter: '^#ServerName'
    line: ServerName www.example.com

- name: Create file if it doesn't exist
  pdutton.xplat.lineinfile:
    path: /tmp/myconfig
    line: key=value
    create: yes
'''

RETURN = r'''
backup:
  description: Name of backup file created, if applicable.
  type: str
  returned: changed and backup=yes
  sample: /etc/hosts.2023-04-13@10:25:28~
msg:
  description: A message about what happened.
  type: str
  returned: always
  sample: line added
'''
