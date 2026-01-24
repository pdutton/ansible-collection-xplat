#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleActionFail


class ActionModule(ActionBase):
    """Cross-platform get_url action plugin.

    Abstracts differences between ansible.builtin.get_url (Linux/Mac) and
    ansible.windows.win_get_url (Windows) by detecting the target OS and
    delegating to the appropriate module.
    """

    TRANSFERS_FILES = False

    def run(self, tmp=None, task_vars=None):
        """Execute the action plugin.

        Args:
            tmp: Temporary directory on remote host
            task_vars: Variables available to the task

        Returns:
            Dictionary containing the module result
        """
        super(ActionModule, self).run(tmp, task_vars)

        if task_vars is None:
            task_vars = {}

        # Validate required parameters
        if 'url' not in self._task.args:
            raise AnsibleActionFail('url is required for pdutton.xplat.get_url')

        if 'dest' not in self._task.args:
            raise AnsibleActionFail('dest is required for pdutton.xplat.get_url')

        # Detect target OS from task variables
        os_family = task_vars.get('ansible_os_family', '').lower()
        system = task_vars.get('ansible_system', '').lower()

        # Determine which module to use
        if os_family == 'windows' or system == 'win32nt':
            module_name = 'ansible.windows.win_get_url'
        else:
            module_name = 'ansible.builtin.get_url'

        # Prepare module arguments - pass through all task arguments
        module_args = self._task.args.copy()

        # Execute the appropriate module
        result = self._execute_module(
            module_name=module_name,
            module_args=module_args,
            task_vars=task_vars,
            tmp=tmp
        )

        return result
