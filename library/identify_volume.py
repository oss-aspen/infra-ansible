#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.module_utils.basic import AnsibleModule

# --- Ansible Module Documentation ---
DOCUMENTATION = r'''
---
module: find_aws_volume
short_description: Finds the AWS Volume ID for a given mount point.
description:
  - This module inspects a local mount point, determines its underlying root block device,
    and retrieves the device's serial number, which corresponds to the AWS EBS Volume ID.
options:
  mount_point:
    description: The absolute path of the mounted filesystem to inspect.
    required: true
    type: str
author:
    - Adrian Edwards (@MoralCode)
'''

EXAMPLES = r'''
- name: Find the volume ID for the /data mount
  find_aws_volume:
    mount_point: /data
  register: volume_info

- name: Display the found volume ID
  ansible.builtin.debug:
    msg: "The AWS Volume ID is {{ volume_info.aws_volume_id }}"
'''

RETURN = r'''
aws_volume_id:
  description: The AWS-formatted EBS Volume ID.
  returned: on success
  type: str
  sample: "vol-012345abcdef6789"
root_block_device:
  description: The root block device for the mount point (e.g., /dev/nvme0n1).
  returned: on success
  type: str
  sample: "/dev/nvme0n1"
'''
# --- End of Documentation ---



def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        mount_point=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = False

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # nothing should ever change as a result of this module
    result['changed'] = False

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()