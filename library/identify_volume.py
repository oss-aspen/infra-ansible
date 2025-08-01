#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.module_utils.basic import AnsibleModule

# --- Ansible Module Documentation ---
DOCUMENTATION = r'''
---
module: find_aws_volume_from_device
short_description: Finds the AWS Volume ID for a given block device name.
description:
  - This module inspects a local block device and retrieves it's serial number,
  which corresponds to the AWS EBS Volume ID.
options:
  partition_device:
    description: The block device to inspect (e.g., /dev/nvme0n1p1), if available.
    required: false
    type: str
author:
    - Adrian Edwards (@MoralCode)
'''

EXAMPLES = r'''
- name: Find the volume ID for a specific device
  find_aws_volume_from_device:
    partition_device: /dev/nvme1n1p1
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
'''
# --- End of Documentation ---

def run_command(module, cmd):
    """Helper function to run a shell command."""
    rc, stdout, stderr = module.run_command(cmd, check_rc=False)
    if rc != 0:
        module.fail_json(msg=f"Command failed: {cmd}", stderr=stderr)
    return stdout.strip()


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        partition_device=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    partition_device = module.params['partition_device']
    
    # 1. Find the partition device for the mount point (replaces `selectattr` task)

    # 2. Find the parent device using lsblk (replaces `lsblk -no pkname` task)
    # This handles cases where the device is a partition (e.g., /dev/sda1)
    cmd = f"lsblk -no pkname {partition_device}"
    rc, stdout, stderr = module.run_command(cmd, check_rc=False)
    if rc == 32: # none of specified devices found
        # return without setting a volume ID
        module.exit_json(**result)
    elif rc != 0:
        module.fail_json(msg=f"Command failed: {cmd}", stderr=stderr)
   
    pkname = stdout.strip()

    if not pkname.startswith("/dev"):
        root_block_device = f"/dev/{pkname}"
    else:
        root_block_device = partition_device

    # 3. Get the serial number (volume ID) for the root device
    serial = run_command(module, f"lsblk -o SERIAL -n -d {root_block_device}")

    if not serial:
        module.fail_json(msg=f"Could not retrieve serial number for device '{root_block_device}'.")

    # 4. Transform the serial number into the standard AWS Volume ID format
    aws_volume_id = serial
    # The serial for EBS volumes is 'vol<id>', but the API needs 'vol-<id>'
    if serial.startswith('vol') and '-' not in serial:
        aws_volume_id = 'vol-' + serial[3:]

    # Prepare the results to return
    result["aws_volume_id"] = aws_volume_id

    # Exit successfully, returning the result
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()