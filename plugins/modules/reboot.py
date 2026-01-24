#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: reboot
short_description: Reboot a machine
description:
  - This module is a cross-platform wrapper that abstracts differences between
    ansible.builtin.reboot (used on Linux and macOS) and ansible.windows.win_reboot
    (used on Windows).
  - It provides a consistent interface for rebooting machines across all platforms.
  - The actual implementation delegates to the appropriate platform-specific module.
  - Reboots the machine and waits for it to come back online.

options:
  reboot_timeout:
    description:
      - Maximum seconds to wait for machine to reboot and respond to a test command.
    type: int
    default: 600

  pre_reboot_delay:
    description:
      - Seconds to wait before reboot.
    type: int
    default: 0

  post_reboot_delay:
    description:
      - Seconds to wait after the reboot command was successful before
        attempting to validate the system rebooted.
    type: int
    default: 0

  connect_timeout:
    description:
      - Maximum seconds to wait for a successful connection to the managed hosts
        before trying again.
    type: int
    default: 5

  test_command:
    description:
      - Command to run to check if machine is ready.
      - Only applies to Unix systems.
    type: str
    default: whoami

  msg:
    description:
      - Message to display to users before reboot.
    type: str
    default: Reboot initiated by Ansible

  boot_time_command:
    description:
      - Command to run to get the boot time.
      - Only applies to Unix systems.
    type: str

author:
  - Paul Dutton (@pdutton)

notes:
  - This is an action plugin that delegates to platform-specific modules.
  - For Linux/macOS uses ansible.builtin.reboot
  - For Windows uses ansible.windows.win_reboot
  - The connection will be interrupted during the reboot process.
'''

EXAMPLES = r'''
- name: Reboot the machine
  pdutton.xplat.reboot:

- name: Reboot with a longer timeout
  pdutton.xplat.reboot:
    reboot_timeout: 900

- name: Reboot with delay
  pdutton.xplat.reboot:
    pre_reboot_delay: 30
    post_reboot_delay: 60

- name: Reboot with custom message
  pdutton.xplat.reboot:
    msg: "System reboot for maintenance"
'''

RETURN = r'''
rebooted:
  description: Whether the machine was rebooted.
  type: bool
  returned: always
  sample: true
elapsed:
  description: The number of seconds that elapsed waiting for the system to be rebooted.
  type: int
  returned: always
  sample: 120
'''
