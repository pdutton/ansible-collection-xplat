#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: get_url
short_description: Download files from HTTP, HTTPS, or FTP
description:
  - This module is a cross-platform wrapper that abstracts differences between
    ansible.builtin.get_url (used on Linux and macOS) and ansible.windows.win_get_url
    (used on Windows).
  - It provides a consistent interface for downloading files across all platforms.
  - The actual implementation delegates to the appropriate platform-specific module.

options:
  url:
    description:
      - HTTP, HTTPS, or FTP URL to download from.
    type: str
    required: true

  dest:
    description:
      - Absolute path of where to download the file to.
      - If dest is a directory, the basename of the file on the remote server
        will be used.
    type: path
    required: true

  force:
    description:
      - If C(true), will download the file every time and replace if different.
      - If C(false), will only download if the destination does not exist.
    type: bool
    default: false

  checksum:
    description:
      - If a checksum is passed, the file will be validated after download.
      - Format is algorithm:checksum, e.g., sha256:abc123...
    type: str

  timeout:
    description:
      - Timeout in seconds for URL request.
    type: int
    default: 10

  headers:
    description:
      - Add custom HTTP headers to a request in hash/dict format.
    type: dict

  url_username:
    description:
      - The username for HTTP basic authentication.
    type: str

  url_password:
    description:
      - The password for HTTP basic authentication.
    type: str

  validate_certs:
    description:
      - If C(false), SSL certificates will not be validated.
    type: bool
    default: true

  mode:
    description:
      - The permissions of the destination file.
      - For Unix systems, use octal numbers (e.g., C(0644)) or symbolic mode.
      - For Windows, this parameter is ignored.
    type: raw

  owner:
    description:
      - Name of the user that should own the file on Unix systems.
      - For Windows, this parameter is ignored.
    type: str

  group:
    description:
      - Name of the group that should own the file on Unix systems.
      - For Windows, this parameter is ignored.
    type: str

author:
  - Paul Dutton (@pdutton)

notes:
  - This is an action plugin that delegates to platform-specific modules.
  - For Linux/macOS uses ansible.builtin.get_url
  - For Windows uses ansible.windows.win_get_url
  - Some parameters like mode, owner, and group only apply to Unix systems.
'''

EXAMPLES = r'''
- name: Download a file
  pdutton.xplat.get_url:
    url: https://example.com/file.tar.gz
    dest: /tmp/file.tar.gz

- name: Download with checksum validation
  pdutton.xplat.get_url:
    url: https://example.com/file.zip
    dest: /tmp/file.zip
    checksum: sha256:abc123def456...

- name: Download with authentication
  pdutton.xplat.get_url:
    url: https://secure.example.com/file.bin
    dest: /opt/files/file.bin
    url_username: myuser
    url_password: mypassword

- name: Download with custom headers
  pdutton.xplat.get_url:
    url: https://api.example.com/download
    dest: /tmp/data.json
    headers:
      Authorization: Bearer mytoken
'''

RETURN = r'''
dest:
  description: Destination file path.
  type: str
  returned: success
  sample: /tmp/file.tar.gz
url:
  description: The URL that was requested.
  type: str
  returned: always
  sample: https://example.com/file.tar.gz
checksum_dest:
  description: Checksum of the destination file after download.
  type: str
  returned: success
  sample: 6e642bb8dd5c2e027bf21dd923337cbb4214f827
checksum_src:
  description: Checksum of the source file (if available).
  type: str
  returned: success
  sample: 6e642bb8dd5c2e027bf21dd923337cbb4214f827
size:
  description: Size of the file after download.
  type: int
  returned: success
  sample: 12345
status_code:
  description: HTTP status code of the response.
  type: int
  returned: always
  sample: 200
'''
