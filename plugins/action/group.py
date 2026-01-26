#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleActionFail


class ActionModule(ActionBase):
    """Cross-platform group action plugin.

    Abstracts differences between ansible.builtin.group (Linux/Mac) and
    ansible.windows.win_group (Windows) by detecting the target OS and
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
        if 'name' not in self._task.args:
            raise AnsibleActionFail('name is required for pdutton.xplat.group')

        # Detect target OS from task variables
        os_family = task_vars.get('ansible_os_family', '').lower()
        system = task_vars.get('ansible_system', '').lower()

        # Determine which module to use
        if os_family == 'windows' or system == 'win32nt':
            module_name = 'ansible.windows.win_group'
        else:
            module_name = 'ansible.builtin.group'

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
