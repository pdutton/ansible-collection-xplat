#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import posixpath
import ntpath


def basename_filter(path):
    """Extract basename from path, handling both Unix and Windows formats.

    This filter automatically detects whether the input path is in Unix or
    Windows format by looking for Windows-specific patterns (backslashes,
    drive letters, UNC prefixes) and applies the appropriate basename logic.

    Args:
        path: A path string in either Unix or Windows format

    Returns:
        The basename of the path (the final component after the last
        separator). Trailing slashes result in an empty string, matching
        the behavior of os.path.basename().

    Examples:
        '/etc/hostname' -> 'hostname'
        'C:\\Windows\\System32\\cmd.exe' -> 'cmd.exe'
        '/path/to/file/' -> ''
        '\\\\server\\share\\file.txt' -> 'file.txt'
    """
    # Input validation - coerce to string if needed
    if not isinstance(path, str):
        path = str(path)

    # Detect Windows path by looking for:
    # 1. Backslash character
    # 2. Drive letter (character at position 1 is ':')
    # 3. UNC path prefix ('\\')
    is_windows_path = (
        '\\' in path or
        (len(path) >= 2 and path[1] == ':') or
        path.startswith('\\\\')
    )

    # Apply appropriate basename function based on detected format
    if is_windows_path:
        return ntpath.basename(path)
    else:
        return posixpath.basename(path)


class FilterModule(object):
    """Ansible filter plugin for cross-platform path operations."""

    def filters(self):
        """Return dict of filter names mapped to functions."""
        return {
            'basename': basename_filter,
            'xplat_basename': basename_filter
        }
