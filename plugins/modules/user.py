#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: user
short_description: Manage user accounts
description:
  - This module is a cross-platform wrapper that abstracts differences between
    ansible.builtin.user (used on Linux and macOS) and ansible.windows.win_user
    (used on Windows).
  - It provides a consistent interface for managing user accounts across all platforms.
  - The actual implementation delegates to the appropriate platform-specific module.

options:
  name:
    description:
      - Name of the user to create, remove or modify.
    type: str
    required: true

  state:
    description:
      - Whether the account should exist or not.
    type: str
    choices: [absent, present]
    default: present

  password:
    description:
      - Password for the user.
      - On Linux, this is the hashed password.
      - On Windows, this is the plaintext password.
    type: str

  update_password:
    description:
      - When to update the password.
      - C(always) will update passwords if they differ.
      - C(on_create) will only set password for new users.
    type: str
    choices: [always, on_create]
    default: always

  uid:
    description:
      - User ID for the user.
      - Only applies to Unix systems.
    type: int

  group:
    description:
      - Primary group for the user.
      - Only applies to Unix systems.
    type: str

  groups:
    description:
      - List of groups user will be added to.
    type: list
    elements: str

  append:
    description:
      - If C(true), add the user to the groups specified in C(groups).
      - If C(false), user will only be added to the groups specified,
        removing them from all other groups.
    type: bool
    default: false

  home:
    description:
      - Home directory of the user.
      - Only applies to Unix systems.
    type: path

  create_home:
    description:
      - When creating a user, create their home directory.
      - Only applies to Unix systems.
    type: bool
    default: true

  shell:
    description:
      - Login shell of the user.
      - Only applies to Unix systems.
    type: str

  comment:
    description:
      - Comment/description of the user (GECOS field on Unix).
    type: str

  expires:
    description:
      - An expiry time for the user.
      - On Unix, this is an epoch timestamp.
      - On Windows, specify a valid datetime value.
    type: str

  password_never_expires:
    description:
      - C(true) if password should never expire.
      - Only applies to Windows systems.
    type: bool

  user_cannot_change_password:
    description:
      - C(true) if user cannot change their password.
      - Only applies to Windows systems.
    type: bool

  account_disabled:
    description:
      - C(true) if account should be disabled.
      - Only applies to Windows systems.
    type: bool

  account_locked:
    description:
      - C(true) to lock the account.
      - Only applies to Windows systems.
    type: bool

author:
  - Paul Dutton (@pdutton)

notes:
  - This is an action plugin that delegates to platform-specific modules.
  - For Linux/macOS uses ansible.builtin.user
  - For Windows uses ansible.windows.win_user
  - Some parameters only apply to specific platforms as noted.
  - Password handling differs between platforms.
'''

EXAMPLES = r'''
- name: Create a user
  pdutton.xplat.user:
    name: johnd
    comment: John Doe
    state: present

- name: Remove a user
  pdutton.xplat.user:
    name: johnd
    state: absent

- name: Create user with specific groups
  pdutton.xplat.user:
    name: johnd
    groups:
      - wheel
      - developers
    append: yes

- name: Create user with password (Unix)
  pdutton.xplat.user:
    name: johnd
    password: "{{ 'mypassword' | password_hash('sha512') }}"

- name: Create user on Windows
  pdutton.xplat.user:
    name: johnd
    password: SecurePassword123!
    groups:
      - Administrators
'''

RETURN = r'''
name:
  description: The name of the user.
  type: str
  returned: always
  sample: johnd
state:
  description: The state of the user account.
  type: str
  returned: always
  sample: present
uid:
  description: The user ID (Unix only).
  type: int
  returned: Unix only
  sample: 1001
group:
  description: Primary group ID (Unix only).
  type: int
  returned: Unix only
  sample: 1001
home:
  description: Home directory path.
  type: str
  returned: when applicable
  sample: /home/johnd
'''
