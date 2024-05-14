from typing import Callable

class Action:
    """
    Actions are performed by Characters in an Environment. They have an effect and can contain a condition function.
    """

    def __init__(self, name: str, effect: Callable = None, condition: Callable = None) -> None:
        """
        Creates a new action, which can be performed by any Character in a given Environment.

        Args:
            name (str): Action name
            effect (Callable, optional): Action's effect function. Defaults to None.
            condition (Callable, optional): Action's condition function. Must return a boolean value. Defaults to None.
        """        
        self.name = name
        self.effect = effect
        self.condition = condition

    def perform(self, actor: 'Character', environment: 'Environment', *args, **kwargs) -> None:
        """Performs the action if the condition is met.

        Args:
            actor (Character): Character performing the action.
            environment (Environment): Environment where the action is being performed.
        """        
        if self.check_condition(actor, environment, *args, **kwargs):
            self.effect(actor, environment, *args, **kwargs)
        del self

    def check_condition(self, actor: 'Character', environment: 'Environment', *args, **kwargs) -> bool:
        """Checks if the action can actually be performed.

        Args:
            actor (Character): Character performing the action.
            environment (Environment): Environment where the action is being performed.

        Returns:
            bool: True if the condition is met, False otherwise. If action has no condition, it always returns True.
        """        
        if self.condition:
            return self.condition(actor, environment)
        return True
