from character import Character

class Environment():
    """
    The Environment class represents a place where the characters can interact with each other and the world.
    """

    def __init__(self, name: str, superior_environment: 'Environment', contiguous_environments: list, default_status: dict, possible_actions: list, upward_action_blocker: bool = True) -> None:
        """Creates a new environment.

        Args:
            name (str): Name of the new environment.
            superior_environment (Environment): Environment that encapsulates this one.
            contiguous_environments (list): Contiguous environments to this one.
            default_status (dict): Status of the environment.
            possible_actions (list): Possible actions that can be performed in this environment.
            upward_action_blocker (bool, optional): True if blocks possible actions from superior environments. Defaults to True.
        """
        self.name = name
        self.superior_environment = superior_environment
        self.status = default_status
        self.possible_actions = possible_actions
        self.current_characters = []
        self.contiguous_environments = contiguous_environments
        self.image = None
        # TODO - upward action blocker

    def add_superior_environment(self, environment: 'Environment'):
        """Adds a superior environment to this environment.

        Args:
            environment (Environment): Environment to be added as superior.
        """
        if environment != self.superior_environment:
            self.superior_environment = environment

    def remove_superior_environment(self):
        """Removes the superior environment from this environment.
        """
        self.superior_environment = None

    def move_players_to_superior_environment(self):
        """Moves all players in this environment to the superior environment.
        """
        for character in self.current_characters:
            if character.status.get("type") == "player":
                character.change_environment(self.superior_environment)

    # TODO - Remove by name?

    def add_contiguous_environment(self, environment: 'Environment'):
        """Adds a contiguous environment to this environment.

        Args:
            environment (Environment): Environment to be added as contiguous.
        """
        if environment not in self.contiguous_environments:
            self.contiguous_environments.append(environment)

    def remove_contiguous_environment(self, environment: 'Environment'):
        """Removes a contiguous environment from this environment.

        Args:
            environment (Environment): Environment to be removed.
        """
        if environment in self.contiguous_environments:
            self.contiguous_environments.remove(environment)

    def add_character(self, character: 'Character'):
        """Adds a character to the environment.

        Args:
            character (Character): Character to be added.
        """
        if character not in self.current_characters:
            self.current_characters.append(character)

    def remove_character(self, character: 'Character'):
        """Removes a character from the environment.

        Args:
            character (Character): Character to be removed.
        """
        if character in self.current_characters:
            self.current_characters.remove(character)

    def get_characters_of_type(self, character_type: str) -> list:
        """Returns a list of characters of a certain type in the environment.

        Args:
            character_type (str): Type of character to search for.

        Returns:
            list: List of characters of the specified type.
        """
        return [char for char in self.current_characters if char.status.get("type") == character_type]
    
    def get_character_by_name(self, name: str) -> Character:
        """Returns a character with the specified name.

        Args:
            name (str): Name of the character to search for.

        Returns:
            Character: Character with the specified name.
        """
        for character in self.current_characters:
            if character.name == name:
                return character

    def destroy(self):
        """Completely destroys the environment, eliminating itself and all references to it.
        """
        for character in self.current_characters:
            character.change_environment(self.superior_environment)
        for env in self.contiguous_environments:
            env.remove_contiguous_environment(self)
