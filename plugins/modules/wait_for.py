#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: wait_for
short_description: Waits for a condition before continuing
description:
  - This module is a cross-platform wrapper that abstracts differences between
    ansible.builtin.wait_for (used on Linux and macOS) and ansible.windows.win_wait_for
    (used on Windows).
  - It provides a consistent interface for waiting on conditions across all platforms.
  - The actual implementation delegates to the appropriate platform-specific module.
  - Can wait for a port to become available, a file to exist, or a search string
    to appear in a file.

options:
  host:
    description:
      - A resolvable hostname or IP address to wait for.
    type: str
    default: 127.0.0.1

  port:
    description:
      - Port number to wait for.
    type: int

  path:
    description:
      - Path to a file on the filesystem to wait for.
    type: path

  search_regex:
    description:
      - A regex pattern to search for in the file at C(path).
      - Also used when waiting for a port with C(state=drained).
    type: str

  state:
    description:
      - C(present) - wait for a port to be open or file to exist.
      - C(started) - alias for C(present).
      - C(stopped) - wait for a port to be closed.
      - C(absent) - wait for a file or port to be absent.
      - C(drained) - wait for active connections to be drained on the port.
    type: str
    choices: [absent, drained, present, started, stopped]
    default: started

  timeout:
    description:
      - Maximum number of seconds to wait for.
    type: int
    default: 300

  delay:
    description:
      - Number of seconds to wait before starting to poll.
    type: int
    default: 0

  sleep:
    description:
      - Number of seconds to sleep between checks.
    type: int
    default: 1

  connect_timeout:
    description:
      - Maximum number of seconds to wait for a connection to happen.
    type: int
    default: 5

  msg:
    description:
      - This overrides the normal error message from a failure.
    type: str

  exclude_hosts:
    description:
      - List of hosts to ignore when looking for active TCP connections.
      - Only used with C(state=drained).
    type: list
    elements: str

author:
  - Paul Dutton (@pdutton)

notes:
  - This is an action plugin that delegates to platform-specific modules.
  - For Linux/macOS uses ansible.builtin.wait_for
  - For Windows uses ansible.windows.win_wait_for
  - The module returns as soon as the condition is met.
'''

EXAMPLES = r'''
- name: Wait for port 8080 to be open
  pdutton.xplat.wait_for:
    port: 8080
    state: started

- name: Wait for port to close
  pdutton.xplat.wait_for:
    port: 8080
    state: stopped

- name: Wait for file to exist
  pdutton.xplat.wait_for:
    path: /tmp/ready.txt

- name: Wait for file to contain specific text
  pdutton.xplat.wait_for:
    path: /var/log/app.log
    search_regex: "Application started"

- name: Wait with custom timeout
  pdutton.xplat.wait_for:
    port: 3306
    timeout: 600
    delay: 10

- name: Wait for connections to drain
  pdutton.xplat.wait_for:
    port: 80
    state: drained
    exclude_hosts:
      - 10.0.0.1
'''

RETURN = r'''
elapsed:
  description: The number of seconds that elapsed while waiting.
  type: int
  returned: always
  sample: 23
match_groups:
  description: When using a regex search, the matched groups.
  type: list
  returned: when using search_regex
  sample: ["match1", "match2"]
match_groupdict:
  description: When using a named regex search, the matched named groups.
  type: dict
  returned: when using named regex groups
  sample: {"name": "value"}
'''
