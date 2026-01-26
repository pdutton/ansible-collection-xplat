#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: uri
short_description: Interacts with webservices
description:
  - This module is a cross-platform wrapper that abstracts differences between
    ansible.builtin.uri (used on Linux and macOS) and ansible.windows.win_uri
    (used on Windows).
  - It provides a consistent interface for making HTTP requests across all platforms.
  - The actual implementation delegates to the appropriate platform-specific module.

options:
  url:
    description:
      - HTTP or HTTPS URL to make a request to.
    type: str
    required: true

  method:
    description:
      - The HTTP method of the request.
    type: str
    choices: [GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS, CONNECT, TRACE]
    default: GET

  body:
    description:
      - The body of the HTTP request/response.
    type: raw

  body_format:
    description:
      - The serialization format of the body.
    type: str
    choices: [form-urlencoded, json, raw, form-multipart]
    default: raw

  headers:
    description:
      - Dictionary of HTTP headers.
    type: dict

  url_username:
    description:
      - Username for HTTP basic authentication.
    type: str

  url_password:
    description:
      - Password for HTTP basic authentication.
    type: str

  force_basic_auth:
    description:
      - Force sending of Basic authentication header.
    type: bool
    default: false

  validate_certs:
    description:
      - If C(false), SSL certificates will not be validated.
    type: bool
    default: true

  timeout:
    description:
      - The socket level timeout in seconds.
    type: int
    default: 30

  status_code:
    description:
      - List of valid, numeric HTTP status codes that signify success.
    type: list
    elements: int
    default: [200]

  return_content:
    description:
      - Whether to return the body content as the C(content) key in the result.
    type: bool
    default: false

  follow_redirects:
    description:
      - Whether to follow redirects.
    type: str
    choices: [all, none, safe, urllib2]
    default: safe

  dest:
    description:
      - Path to download the file to.
    type: path

  creates:
    description:
      - A filename, when it already exists, this step will not run.
    type: path

  removes:
    description:
      - A filename, when it does not exist, this step will not run.
    type: path

author:
  - Paul Dutton (@pdutton)

notes:
  - This is an action plugin that delegates to platform-specific modules.
  - For Linux/macOS uses ansible.builtin.uri
  - For Windows uses ansible.windows.win_uri
'''

EXAMPLES = r'''
- name: Make a GET request
  pdutton.xplat.uri:
    url: https://api.example.com/data
  register: result

- name: Make a POST request with JSON body
  pdutton.xplat.uri:
    url: https://api.example.com/data
    method: POST
    body:
      name: test
      value: 123
    body_format: json
    headers:
      Content-Type: application/json

- name: Download a file
  pdutton.xplat.uri:
    url: https://example.com/file.zip
    dest: /tmp/file.zip

- name: Check website is up
  pdutton.xplat.uri:
    url: https://example.com
    method: HEAD
    status_code: [200, 301, 302]

- name: Make authenticated request
  pdutton.xplat.uri:
    url: https://api.example.com/private
    url_username: myuser
    url_password: mypassword
    force_basic_auth: yes
'''

RETURN = r'''
status:
  description: The HTTP status code from the request.
  type: int
  returned: always
  sample: 200
url:
  description: The URL that was actually requested.
  type: str
  returned: always
  sample: https://api.example.com/data
content:
  description: The response body content.
  type: str
  returned: when return_content=true
  sample: '{"key": "value"}'
json:
  description: The response body parsed as JSON.
  type: dict
  returned: when Content-Type is application/json
  sample: {"key": "value"}
redirected:
  description: Whether the request was redirected.
  type: bool
  returned: always
  sample: false
elapsed:
  description: The number of seconds that elapsed while performing the download.
  type: int
  returned: always
  sample: 2
'''
