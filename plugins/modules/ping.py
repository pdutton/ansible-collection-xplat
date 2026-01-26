#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ping
short_description: Try to connect to host and verify a usable Python
description:
  - This module is a cross-platform wrapper that abstracts differences between
    ansible.builtin.ping (used on Linux and macOS) and ansible.windows.win_ping
    (used on Windows).
  - It provides a consistent interface for testing connectivity across all platforms.
  - The actual implementation delegates to the appropriate platform-specific module.
  - A trivial test module that does not use ICMP, only verifies connectivity.

options:
  data:
    description:
      - Data to return for the ping return value.
      - If this parameter is set to C(crash), the module will cause an exception.
    type: str
    default: pong

author:
  - Paul Dutton (@pdutton)

notes:
  - This is an action plugin that delegates to platform-specific modules.
  - For Linux/macOS uses ansible.builtin.ping
  - For Windows uses ansible.windows.win_ping
  - This is NOT ICMP ping, this is just a trivial test module to verify
    the Ansible connection and Python work.
'''

EXAMPLES = r'''
- name: Test connectivity
  pdutton.xplat.ping:

- name: Test connectivity with custom return data
  pdutton.xplat.ping:
    data: hello

- name: Verify connection works
  pdutton.xplat.ping:
  register: result

- name: Debug ping result
  ansible.builtin.debug:
    var: result.ping
'''

RETURN = r'''
ping:
  description: Value provided with the C(data) parameter.
  type: str
  returned: success
  sample: pong
'''
