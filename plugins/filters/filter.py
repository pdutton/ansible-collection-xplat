#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import posixpath
import ntpath


def _is_windows_path(path):
    """Detect if a path string is in Windows format.

    Windows paths are detected by looking for:
    1. Backslash character
    2. Drive letter (character at position 1 is ':')
    3. UNC path prefix ('\\')

    Args:
        path: A path string

    Returns:
        True if the path appears to be Windows format, False otherwise
    """
    return (
        '\\' in path or
        (len(path) >= 2 and path[1] == ':') or
        path.startswith('\\\\')
    )


def basename_filter(path):
    """Extract basename from path, handling both Unix and Windows formats.

    This filter automatically detects whether the input path is in Unix or
    Windows format and applies the appropriate basename logic.

    Args:
        path: A path string in either Unix or Windows format

    Returns:
        The basename of the path (the final component after the last
        separator). Trailing slashes result in an empty string.

    Examples:
        '/etc/hostname' -> 'hostname'
        'C:\\Windows\\System32\\cmd.exe' -> 'cmd.exe'
        '/path/to/file/' -> ''
        '\\\\server\\share\\file.txt' -> 'file.txt'
    """
    if not isinstance(path, str):
        path = str(path)

    if _is_windows_path(path):
        return ntpath.basename(path)
    else:
        return posixpath.basename(path)


def dirname_filter(path):
    """Extract directory name from path, handling both Unix and Windows formats.

    This filter automatically detects whether the input path is in Unix or
    Windows format and applies the appropriate dirname logic.

    Args:
        path: A path string in either Unix or Windows format

    Returns:
        The directory portion of the path (everything before the final
        component). Returns empty string for paths without directory.

    Examples:
        '/etc/hostname' -> '/etc'
        'C:\\Windows\\System32\\cmd.exe' -> 'C:\\Windows\\System32'
        'filename.txt' -> ''
        '\\\\server\\share\\file.txt' -> '\\\\server\\share'
    """
    if not isinstance(path, str):
        path = str(path)

    if _is_windows_path(path):
        return ntpath.dirname(path)
    else:
        return posixpath.dirname(path)


def splitext_filter(path):
    """Split path into root and extension, handling both Unix and Windows formats.

    This filter automatically detects whether the input path is in Unix or
    Windows format and applies the appropriate splitext logic.

    Args:
        path: A path string in either Unix or Windows format

    Returns:
        A list containing [root, extension]. The extension includes the
        leading dot. If there is no extension, returns [path, ''].

    Examples:
        '/etc/hostname.conf' -> ['/etc/hostname', '.conf']
        'C:\\Windows\\System32\\cmd.exe' -> ['C:\\Windows\\System32\\cmd', '.exe']
        'filename' -> ['filename', '']
        '.bashrc' -> ['.bashrc', '']
    """
    if not isinstance(path, str):
        path = str(path)

    if _is_windows_path(path):
        result = ntpath.splitext(path)
    else:
        result = posixpath.splitext(path)

    # Return as list for Jinja2 compatibility
    return list(result)


def join_filter(base, *parts):
    """Join path components, handling both Unix and Windows formats.

    This filter automatically detects whether the base path is in Unix or
    Windows format and applies the appropriate join logic.

    Args:
        base: The base path string (determines path format)
        *parts: Additional path components to join

    Returns:
        The joined path string using the appropriate separator.

    Examples:
        join('/etc', 'hostname') -> '/etc/hostname'
        join('C:\\Windows', 'System32', 'cmd.exe') -> 'C:\\Windows\\System32\\cmd.exe'
        join('/home', 'user', 'documents') -> '/home/user/documents'
    """
    if not isinstance(base, str):
        base = str(base)

    # Convert all parts to strings
    str_parts = [str(p) for p in parts]

    if _is_windows_path(base):
        return ntpath.join(base, *str_parts)
    else:
        return posixpath.join(base, *str_parts)


class FilterModule(object):
    """Ansible filter plugin for cross-platform path operations."""

    def filters(self):
        """Return dict of filter names mapped to functions."""
        return {
            'basename': basename_filter,
            'xplat_basename': basename_filter,
            'dirname': dirname_filter,
            'xplat_dirname': dirname_filter,
            'splitext': splitext_filter,
            'xplat_splitext': splitext_filter,
            'join': join_filter,
            'xplat_join': join_filter,
        }
