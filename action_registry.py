import importlib
import inspect
import action as a

def format_action_name(function_name: str) -> str:
    """Formats the action name to a human-readable format.

    Args:
        function_name (str): The lowercased, underscore-separated action name.

    Returns:
        str: The human-readable action name.

    Example:
        >>> format_action_name('my_action_name')
        'My Action Name'
    """
    parts = function_name.split('_')
    return ' '.join(part.capitalize() for part in parts)

class ActionRegistry:
    """
    Registry for actions. It allows to register and retrieve actions by name. Actions are only instanced when used by a Character.
    """    
    def __init__(self, module_path: str) -> None:
        """
        Initializes the action registry with the module containing the actions.

        Args:
            module_path (str): Path to the Python file which contains both actions and conditions.
        """        
        self.actions = {}
        module_path = module_path.replace('/', '.').rstrip('.py')
        self.module = importlib.import_module(module_path)
        self.register_all_actions()

    def register_action(self, name: str, function_name: str, condition_name: str = None) -> None:
            """Registers an action with its effect and condition functions.

            Args:
                name (str): Action name.
                function_name (str): Name of the function that represents the effect of the action.
                condition_name (str, optional): Name of the boolean function that represents the condition for the action to be executed. Defaults to None.
            """        
            self.actions[name] = {'effect': function_name, 'condition': condition_name}

    def register_all_actions(self) -> None:
        """
        Registers all functions in the module as actions. Functions ending in '_condition' are considered conditions for the previous function.
        """        
        for name, obj in inspect.getmembers(self.module, inspect.isfunction):
            if name.endswith('_condition'):
                action_name = format_action_name(name[:-10])  # Remove '_condition' suffix
                if action_name in self.actions:
                    self.actions[action_name]['condition'] = name
                else:
                    self.actions[action_name] = {'effect': None, 'condition': name}
            else:
                action_name = format_action_name(name)
                if action_name in self.actions:
                    self.actions[action_name]['effect'] = name
                else:
                    self.register_action(action_name, name)

    def get_action(self, name: str) -> a.Action:
        """
        Retrieves an action based on its name.

        Args:
            name (str): The name of the action to retrieve.

        Raises:
            ValueError: If the action is not registered.
            ValueError: If the effect function does not exist.

        Returns:
            a.Action: An instance of the Action class representing the retrieved action.
        """
        metadata = self.actions.get(name)
        if not metadata:
            raise ValueError(f"Action not registered: {name}")

        # Dynamically resolve effect and condition functions from the module
        effect_func = getattr(self.module, metadata['effect'], None)
        condition_func = getattr(self.module, metadata['condition'], None) if metadata['condition'] else None

        if not effect_func:
            raise ValueError("Effect function does not exist")

        # Create an action instance, assuming a class 'Action' exists in module 'action'
        return a.Action(name, effect_func, condition_func)
