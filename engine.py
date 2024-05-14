import action_registry
import constants
import importlib
import environment as e
import sys
import os
from entity_factory import EntityFactory

class Engine():
    
    def __init__(self, module_folder: str = None, entity_storage: str = "INSTANCED") -> None:
        if not module_folder:
            self.module_folder = "."
        else:
            self.module_folder = module_folder
        self.action_registry = action_registry.ActionRegistry(os.path.join(self.module_folder, constants.CODEGEN_ACTIONS_FILENAME))
        self.environments = self.load_environments()
        if entity_storage == "INSTANCED":
            self.entity_storage = EntityFactory()
            self.entity_storage.load_entities(os.path.join(self.module_folder, "config/entities"))

    def load_environments(self):
        # Dictionary to hold environment name to instance mappings
        environments_dict = {}

        # Construct the path to the environments file
        path_to_file = os.path.join(self.module_folder, constants.CODEGEN_ENVIRONMENTS_FILENAME)

        # Dynamically import the module containing the environment instances
        spec = importlib.util.spec_from_file_location("env_module", path_to_file)
        env_module = importlib.util.module_from_spec(spec)
        sys.modules["env_module"] = env_module
        spec.loader.exec_module(env_module)

        # Assuming all variables in the module that are instances of e.Environment should be included
        for attr_name in dir(env_module):
            attr = getattr(env_module, attr_name)
            if isinstance(attr, e.Environment):
                environments_dict[attr.name] = attr

        return environments_dict
    
    def get_environment(self, environment_name: str):
        return self.environments.get(environment_name)
    
    def get_entity(self, entity_name: str):
        return self.entity_storage.get_entity(entity_name)
