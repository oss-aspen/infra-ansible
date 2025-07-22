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

    mount_point = module.params['mount_point']
    
    # 1. Find the partition device for the mount point (replaces `selectattr` task)

    # 2. Find the parent device using lsblk (replaces `lsblk -no pkname` task)
    # This handles cases where the device is a partition (e.g., /dev/sda1)

    # 3. Get the serial number (volume ID) for the root device

    # 4. Transform the serial number into the standard AWS Volume ID format

    # Prepare the results to return

    # Exit successfully, returning the result
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()