#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: group
short_description: Manage groups
description:
  - This module is a cross-platform wrapper that abstracts differences between
    ansible.builtin.group (used on Linux and macOS) and ansible.windows.win_group
    (used on Windows).
  - It provides a consistent interface for managing groups across all platforms.
  - The actual implementation delegates to the appropriate platform-specific module.

options:
  name:
    description:
      - Name of the group to manage.
    type: str
    required: true

  state:
    description:
      - Whether the group should exist or not.
    type: str
    choices: [absent, present]
    default: present

  gid:
    description:
      - Group ID to set for the group.
      - Only applies to Unix systems.
    type: int

  system:
    description:
      - If C(true), create a system group.
      - Only applies to Unix systems.
    type: bool
    default: false

  local:
    description:
      - Forces the use of "local" command alternatives on platforms
        that implement it.
      - Only applies to Unix systems.
    type: bool
    default: false

  non_unique:
    description:
      - Allows setting a non-unique GID.
      - Only applies to Unix systems.
    type: bool
    default: false

author:
  - Paul Dutton (@pdutton)

notes:
  - This is an action plugin that delegates to platform-specific modules.
  - For Linux/macOS uses ansible.builtin.group
  - For Windows uses ansible.windows.win_group
  - Some parameters only apply to specific platforms as noted.
'''

EXAMPLES = r'''
- name: Create a group
  pdutton.xplat.group:
    name: developers
    state: present

- name: Remove a group
  pdutton.xplat.group:
    name: developers
    state: absent

- name: Create a group with specific GID (Unix)
  pdutton.xplat.group:
    name: developers
    gid: 1500
    state: present

- name: Create a system group (Unix)
  pdutton.xplat.group:
    name: myservice
    system: yes
    state: present
'''

RETURN = r'''
name:
  description: The name of the group.
  type: str
  returned: always
  sample: developers
state:
  description: The state of the group.
  type: str
  returned: always
  sample: present
gid:
  description: The group ID (Unix only).
  type: int
  returned: Unix only
  sample: 1500
system:
  description: Whether the group is a system group (Unix only).
  type: bool
  returned: Unix only
  sample: false
'''
