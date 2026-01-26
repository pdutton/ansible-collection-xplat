#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: hostname
short_description: Manage hostname
description:
  - This module is a cross-platform wrapper that abstracts differences between
    ansible.builtin.hostname (used on Linux and macOS) and ansible.windows.win_hostname
    (used on Windows).
  - It provides a consistent interface for managing hostnames across all platforms.
  - The actual implementation delegates to the appropriate platform-specific module.

options:
  name:
    description:
      - Name of the host to set.
    type: str
    required: true

  use:
    description:
      - Which strategy to use to update the hostname.
      - Only applies to Unix systems.
    type: str
    choices: [alpine, debian, freebsd, generic, macos, macosx, darwin, openbsd, openrc, redhat, sles, solaris, systemd]

author:
  - Paul Dutton (@pdutton)

notes:
  - This is an action plugin that delegates to platform-specific modules.
  - For Linux/macOS uses ansible.builtin.hostname
  - For Windows uses ansible.windows.win_hostname
  - A reboot may be required on Windows for the hostname change to take effect.
'''

EXAMPLES = r'''
- name: Set the hostname
  pdutton.xplat.hostname:
    name: myserver.example.com

- name: Set hostname using specific strategy (Unix)
  pdutton.xplat.hostname:
    name: myserver
    use: systemd
'''

RETURN = r'''
name:
  description: The new hostname.
  type: str
  returned: always
  sample: myserver.example.com
reboot_required:
  description: Whether a reboot is required (Windows only).
  type: bool
  returned: Windows only
  sample: true
'''
