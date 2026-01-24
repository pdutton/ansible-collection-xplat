#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleActionFail


class ActionModule(ActionBase):
    """Cross-platform shell action plugin.

    Abstracts differences between ansible.builtin.shell (Linux/Mac) and
    ansible.windows.win_shell (Windows) by detecting the target OS and
    delegating to the appropriate action plugin.
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

        # Determine which action plugin to use
        if os_family == 'windows' or system == 'win32nt':
            action_name = 'ansible.windows.win_shell'
        else:
            action_name = 'ansible.builtin.shell'
            # Convert 'cmd' to '_raw_params' for ansible.builtin.shell
            if 'cmd' in self._task.args and '_raw_params' not in self._task.args:
                self._task.args['_raw_params'] = self._task.args.pop('cmd')

        # Load the appropriate action plugin
        action_loader = self._shared_loader_obj.action_loader
        action_plugin = action_loader.get(
            action_name,
            task=self._task,
            connection=self._connection,
            play_context=self._play_context,
            loader=self._loader,
            templar=self._templar,
            shared_loader_obj=self._shared_loader_obj
        )

        if action_plugin is None:
            raise AnsibleActionFail(f'Could not load action plugin: {action_name}')

        # Execute the action plugin
        result = action_plugin.run(tmp=tmp, task_vars=task_vars)

        return result
