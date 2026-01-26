#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: template
short_description: Template a file out to a remote server
description:
  - This module is a cross-platform wrapper that abstracts differences between
    ansible.builtin.template (used on Linux and macOS) and ansible.windows.win_template
    (used on Windows).
  - It provides a consistent interface for templating files across all platforms.
  - The actual implementation delegates to the appropriate platform-specific module.
  - Templates are processed through the Jinja2 templating language.

options:
  src:
    description:
      - Path of a Jinja2 formatted template on the Ansible controller.
      - This can be a relative or an absolute path.
    type: path
    required: true

  dest:
    description:
      - Location to render the template to on the remote machine.
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

  newline_sequence:
    description:
      - Specify the newline sequence to use for templating files.
    type: str
    choices: ['\n', '\r', '\r\n']
    default: '\n'

  block_start_string:
    description:
      - The string marking the beginning of a block.
    type: str
    default: '{%'

  block_end_string:
    description:
      - The string marking the end of a block.
    type: str
    default: '%}'

  variable_start_string:
    description:
      - The string marking the beginning of a print statement.
    type: str
    default: '{{'

  variable_end_string:
    description:
      - The string marking the end of a print statement.
    type: str
    default: '}}'

  trim_blocks:
    description:
      - Determine when newlines should be removed from blocks.
    type: bool
    default: true

  lstrip_blocks:
    description:
      - Determine when leading spaces and tabs should be stripped.
    type: bool
    default: false

author:
  - Paul Dutton (@pdutton)

notes:
  - This is an action plugin that delegates to platform-specific modules.
  - For Linux/macOS uses ansible.builtin.template
  - For Windows uses ansible.windows.win_template
  - Some parameters like mode, owner, and group only apply to Unix systems.
  - Templates use Jinja2 syntax for variable substitution and logic.
'''

EXAMPLES = r'''
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

- name: Template with Windows line endings
  pdutton.xplat.template:
    src: templates/script.bat.j2
    dest: C:\scripts\script.bat
    newline_sequence: '\r\n'
'''

RETURN = r'''
dest:
  description: Destination file/path.
  type: str
  returned: success
  sample: /etc/myapp/config.conf
src:
  description: Source file used for the template.
  type: str
  returned: changed
  sample: /home/user/templates/myconfig.j2
checksum:
  description: SHA1 checksum of the file after running template.
  type: str
  returned: success
  sample: 6e642bb8dd5c2e027bf21dd923337cbb4214f827
size:
  description: Size of the target file after running template.
  type: int
  returned: success
  sample: 1220
backup_file:
  description: Name of the backup file created when backup=yes.
  type: str
  returned: changed and backup=yes
  sample: /etc/myapp/config.conf.2023-04-13@10:25:28~
'''
