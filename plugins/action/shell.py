#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleActionFail


class ActionModule(ActionBase):
    """Cross-platform shell action plugin.

    Abstracts differences between ansible.builtin.shell (Linux/Mac) and
    ansible.windows.win_shell (Windows) by detecting the target OS and
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
        # The command can be passed as 'cmd' or as free-form '_raw_params'
        if 'cmd' not in self._task.args and '_raw_params' not in self._task.args:
            raise AnsibleActionFail('cmd or free-form command is required for pdutton.xplat.shell')

        # Detect target OS from task variables
        os_family = task_vars.get('ansible_os_family', '').lower()
        system = task_vars.get('ansible_system', '').lower()

        # Determine which module to use
        if os_family == 'windows' or system == 'win32nt':
            # Use Windows shell module
            module_name = 'ansible.windows.win_shell'
        else:
            # Use built-in shell module for Linux, macOS, and other Unix variants
            module_name = 'ansible.builtin.shell'

        # Prepare module arguments - pass through all task arguments
        module_args = self._task.args.copy()

        # The 'cmd' parameter needs to be converted to '_raw_params' for ansible.builtin.shell
        # ansible.windows.win_shell supports 'cmd' directly
        if 'cmd' in module_args and module_name == 'ansible.builtin.shell':
            module_args['_raw_params'] = module_args.pop('cmd')

        # Execute the appropriate module
        result = self._execute_module(
            module_name=module_name,
            module_args=module_args,
            task_vars=task_vars,
            tmp=tmp
        )

        return result
