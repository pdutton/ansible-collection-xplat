#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: service
short_description: Manage services on remote hosts
description:
  - This module is a cross-platform wrapper that abstracts differences between
    ansible.builtin.service (Linux), community.general.launchd (macOS), and
    ansible.windows.win_service (Windows).
  - It provides a consistent interface for managing services across all platforms.
  - The actual implementation delegates to the appropriate platform-specific module.

options:
  name:
    description:
      - Name of the service.
      - On macOS, this is the launchd service label (e.g., C(com.apple.cups.cupsd)).
    type: str
    required: true

  state:
    description:
      - C(started)/C(stopped) are idempotent actions that will not run commands
        unless necessary.
      - C(restarted) will always bounce the service.
      - C(reloaded) will always reload the service (not supported on macOS).
    type: str
    choices: [started, stopped, restarted, reloaded]

  enabled:
    description:
      - Whether the service should start on boot.
    type: bool

  pattern:
    description:
      - If the service does not respond to the status command, name a substring
        to look for as would be found in the output of the C(ps) command.
      - Only applies to Linux systems.
    type: str

  sleep:
    description:
      - If the service is being restarted, this is the number of seconds to sleep
        between the stop and start command.
      - Only applies to Linux systems.
    type: int

  arguments:
    description:
      - Additional arguments provided on the command line.
      - Only applies to Linux systems.
    type: str
    aliases: [args]

  start_mode:
    description:
      - Set the startup type of the service.
      - Only applies to Windows systems.
    type: str
    choices: [auto, delayed, disabled, manual]

  desktop_interact:
    description:
      - Whether to allow the service user to interact with the desktop.
      - Only applies to Windows systems.
    type: bool

author:
  - Paul Dutton (@pdutton)

notes:
  - This is an action plugin that delegates to platform-specific modules.
  - For Linux uses ansible.builtin.service
  - For macOS uses community.general.launchd
  - For Windows uses ansible.windows.win_service
  - Some parameters only apply to specific platforms as noted.
  - Advanced launchd features (force_stop, plist) require using community.general.launchd directly.
'''

EXAMPLES = r'''
# Linux examples
- name: Start a service
  pdutton.xplat.service:
    name: httpd
    state: started

- name: Stop a service
  pdutton.xplat.service:
    name: httpd
    state: stopped

- name: Restart a service
  pdutton.xplat.service:
    name: httpd
    state: restarted

- name: Enable a service to start on boot
  pdutton.xplat.service:
    name: httpd
    enabled: yes

- name: Start and enable a service
  pdutton.xplat.service:
    name: httpd
    state: started
    enabled: yes

# macOS examples (uses launchd)
- name: Start the CUPS printing service on macOS
  pdutton.xplat.service:
    name: com.apple.cups.cupsd
    state: started

- name: Stop a launchd service on macOS
  pdutton.xplat.service:
    name: com.apple.mdnsresponder
    state: stopped

- name: Enable a launchd service to start on boot
  pdutton.xplat.service:
    name: com.apple.ftp-proxy
    enabled: yes
'''

RETURN = r'''
name:
  description: Name of the service.
  type: str
  returned: always
  sample: httpd
state:
  description: Current state of the service.
  type: str
  returned: always
  sample: started
enabled:
  description: Whether the service is enabled to start on boot.
  type: bool
  returned: always
  sample: true
status:
  description: Status information about the service (varies by platform).
  type: dict
  returned: always
'''
