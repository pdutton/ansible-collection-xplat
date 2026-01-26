#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleActionFail


class ActionModule(ActionBase):
    """Cross-platform service action plugin.

    Abstracts differences between ansible.builtin.service (Linux),
    community.general.launchd (macOS), and ansible.windows.win_service (Windows)
    by detecting the target OS and delegating to the appropriate module.
    """

    TRANSFERS_FILES = False

    # Parameters specific to Unix (ansible.builtin.service)
    UNIX_ONLY_PARAMS = {'pattern', 'sleep', 'arguments', 'args'}

    # Parameters specific to Windows (ansible.windows.win_service)
    WINDOWS_ONLY_PARAMS = {'start_mode', 'desktop_interact'}

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
            raise AnsibleActionFail('name is required for pdutton.xplat.service')

        # Detect target OS from task variables
        os_family = task_vars.get('ansible_os_family', '').lower()
        system = task_vars.get('ansible_system', '').lower()

        # Determine which module to use and which parameters to filter
        if os_family == 'windows' or system == 'win32nt':
            module_name = 'ansible.windows.win_service'
            filter_params = self.UNIX_ONLY_PARAMS
        elif os_family == 'darwin' or system == 'darwin':
            module_name = 'community.general.launchd'
            # launchd only supports: name, state, enabled
            filter_params = self.UNIX_ONLY_PARAMS | self.WINDOWS_ONLY_PARAMS
        else:
            module_name = 'ansible.builtin.service'
            filter_params = self.WINDOWS_ONLY_PARAMS

        # Prepare module arguments - pass through task arguments, filtering platform-specific ones
        module_args = {
            k: v for k, v in self._task.args.items()
            if k not in filter_params
        }

        # Execute the appropriate module
        result = self._execute_module(
            module_name=module_name,
            module_args=module_args,
            task_vars=task_vars,
            tmp=tmp
        )

        return result
