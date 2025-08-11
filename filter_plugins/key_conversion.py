from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict
from ansible.errors import AnsibleFilterError

class FilterModule(object):
    """
    Ansible custom filter for converting dictionary keys from camel case to snake case.
    This filter is particularly useful for processing responses from AWS APIs.
    """
    def filters(self):
        return {
            'aws_to_snake_case': self.aws_to_snake_case
        }

    def aws_to_snake_case(self, data):
        """
        Main filter function to convert keys. It leverages Ansible's internal
        utility for robust and consistent transformation.
        """
        # Ensure the input is a dictionary or a list of dictionaries
        if not isinstance(data, (dict, list)):
            raise AnsibleFilterError("The 'aws_to_snake_case' filter must be used on a dictionary or a list of dictionaries.")

        if isinstance(data, list):
            return [camel_dict_to_snake_dict(d) for d in data]
        
        return camel_dict_to_snake_dict(data)