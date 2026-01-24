#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: shell
short_description: Execute shell commands on targets
description:
  - This module is a cross-platform wrapper that abstracts differences between
    ansible.builtin.shell (used on Linux and macOS) and ansible.windows.win_shell
    (used on Windows).
  - It provides a consistent interface for executing shell commands across all platforms.
  - The actual implementation delegates to the appropriate platform-specific module.
  - The shell module takes a command string and processes it through a shell, so
    shell variables, pipes, redirects, and other shell features will work.
  - On Linux/macOS, commands run through /bin/sh by default.
  - On Windows, commands run through PowerShell by default.

options:
  cmd:
    description:
      - The command to run through the shell.
    type: str

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

  executable:
    description:
      - Change the shell used to execute the command.
      - On Linux/macOS, this should be an absolute path to the executable.
      - This option is ignored on Windows.
    type: path

author:
  - Paul Dutton (@pdutton)

notes:
  - This is an action plugin that delegates to platform-specific modules.
  - For Linux/macOS uses ansible.builtin.shell
  - For Windows uses ansible.windows.win_shell
  - If you don't need shell features, consider using the command module instead,
    which is more secure as it doesn't invoke a shell.
'''

EXAMPLES = r'''
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

- name: Run command only if file does not exist
  pdutton.xplat.shell:
    cmd: echo "Creating file" > /tmp/myfile
    creates: /tmp/myfile

- name: Run command with a specific shell
  pdutton.xplat.shell:
    cmd: echo $BASH_VERSION
    executable: /bin/bash
'''

RETURN = r'''
cmd:
  description: The command that was run.
  type: str
  returned: always
  sample: "echo hello"
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
