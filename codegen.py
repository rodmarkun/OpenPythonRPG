import json
import os
import constants

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def generate_actions(json_data):
    python_code = ""
    for action, details in json_data.items():
        function_name = action.replace(' ', '_').lower()
        params = "actor, current_environment"

        if "extra_params" in details:
            params += ", " + ", ".join(details["extra_params"])
            # Generating the _params function if extra_params are present
            python_code += f"def {function_name}_params(actor, current_environment):\n"
            python_code += "    # Define possible parameter lists here\n    pass\n\n"

        python_code += f"def {function_name}({params}):\n"
        python_code += "    # Your code here!\n    pass\n\n"

        if details.get("has_condition", False):
            python_code += f"def {function_name}_condition(actor, current_environment) -> bool:\n"
            python_code += "    return True  # Modify this condition based on your requirements\n\n"
    
    return python_code


def generate_environments(json_data, default_actions):
    python_code = "import environment as e\n\n"
    instances_code = ""
    connections_code = ""
    
    for name, details in json_data.items():
        var_name = name.replace(' ', '_').lower()
        superior_var_name = (details["superior_environment"].replace(' ', '_').lower() if details["superior_environment"] else "None")
        action_list = set(details["possible_actions"]) | set(default_actions)
        # Correctly capitalize each word of the action in the list
        actions = "[" + ", ".join(f'"{action.title()}"' for action in action_list) + "]"
        
        instances_code += f"{var_name} = e.Environment(\"{name}\", {superior_var_name}, [], {details['default_status']}, {actions})\n"

    for name, details in json_data.items():
        var_name = name.replace(' ', '_').lower()
        for contiguous_env in details["contiguous_environments"]:
            contiguous_var_name = contiguous_env.replace(' ', '_').lower()
            connections_code += f"{var_name}.add_contiguous_environment({contiguous_var_name})\n"

    python_code += instances_code + "\n" + connections_code
    return python_code

def write_to_file(module_name, python_code, file_name):
    directory_path = f"modules/{module_name}"
    os.makedirs(directory_path, exist_ok=True)
    file_path = os.path.join(directory_path, file_name)
    
    with open(file_path, 'w') as file:
        file.write(python_code)
    print(f"Code written to {file_path}")

def get_default_actions(json_data):
    # Ensure each word in the action name is capitalized correctly
    return ['_'.join(word.capitalize() for word in action.split(' ')) for action, details in json_data.items() if details.get("default", False)]

# Load JSON data
actions_json = read_json("modules/basic_escordia/config/actions.json")
environments_json = read_json("modules/basic_escordia/config/environments.json")
default_actions = get_default_actions(actions_json)

# Generate and write Python code
write_to_file("basic_escordia", generate_actions(actions_json), constants.CODEGEN_ACTIONS_FILENAME)
write_to_file("basic_escordia", generate_environments(environments_json, default_actions), constants.CODEGEN_ENVIRONMENTS_FILENAME)
