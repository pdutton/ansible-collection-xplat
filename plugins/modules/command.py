#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: command
short_description: Execute commands on targets
description:
  - This module is a cross-platform wrapper that abstracts differences between
    ansible.builtin.command (used on Linux and macOS) and ansible.windows.win_command
    (used on Windows).
  - It provides a consistent interface for executing commands across all platforms.
  - The actual implementation delegates to the appropriate platform-specific module.
  - The command module takes a command name followed by arguments. It will not be
    processed through the shell, so variables and shell operators will not work.

options:
  cmd:
    description:
      - The command to run.
    type: str

  argv:
    description:
      - Passes the command as a list rather than a string.
      - Use C(argv) to avoid quoting values that would otherwise be interpreted.
    type: list
    elements: str

  chdir:
    description:
      - Change into this directory before running the command.
    type: path

  creates:
    description:
      - A filename or glob pattern. If a matching file already exists, the
        command will not run.
    type: path

  removes:
    description:
      - A filename or glob pattern. If a matching file exists, the command
        will run.
    type: path

  stdin:
    description:
      - Set the stdin of the command directly to the specified value.
    type: str

  stdin_add_newline:
    description:
      - If set to C(true), append a newline to stdin data.
    type: bool
    default: true

author:
  - Paul Dutton (@pdutton)

notes:
  - This is an action plugin that delegates to platform-specific modules.
  - For Linux/macOS uses ansible.builtin.command
  - For Windows uses ansible.windows.win_command
  - This module does NOT process commands through a shell. Use the shell module
    if you need shell features like pipes, redirects, or environment variable
    expansion.
'''

EXAMPLES = r'''
- name: Run a simple command
  pdutton.xplat.command:
    cmd: whoami
  register: result

- name: Run command with arguments as list
  pdutton.xplat.command:
    argv:
      - /usr/bin/python3
      - --version
  register: python_version

- name: Run command in specific directory
  pdutton.xplat.command:
    cmd: ls -la
    chdir: /tmp

- name: Run command only if file does not exist
  pdutton.xplat.command:
    cmd: touch /tmp/myfile
    creates: /tmp/myfile
'''

RETURN = r'''
cmd:
  description: The command that was run.
  type: list
  returned: always
  sample: ['echo', 'hello']
rc:
  description: The return code of the command.
  type: int
  returned: always
  sample: 0
stdout:
  description: The standard output of the command.
  type: str
  returned: always
  sample: "Hello World"
stderr:
  description: The standard error of the command.
  type: str
  returned: always
  sample: ""
stdout_lines:
  description: The standard output of the command as a list of lines.
  type: list
  returned: always
  sample: ["Hello World"]
stderr_lines:
  description: The standard error of the command as a list of lines.
  type: list
  returned: always
  sample: []
start:
  description: The time the command started.
  type: str
  returned: always
  sample: "2023-04-13 10:25:28.123456"
end:
  description: The time the command ended.
  type: str
  returned: always
  sample: "2023-04-13 10:25:28.234567"
delta:
  description: The time elapsed running the command.
  type: str
  returned: always
  sample: "0:00:00.111111"
'''
