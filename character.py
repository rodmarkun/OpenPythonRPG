class Character:
    """
    Characters that populate the game world. They can perform actions and change environments. Can be controlled by the player or by the game itself.
    """

    def __init__(self, name: str, status: dict, engine: 'Engine', event_dispatcher: 'EventDispatcher', current_environment: 'Environment', plugins: list, AI_controlled: bool = False) -> None:
        """
        Initializes a new instance of the Character class.

        Args:
            name (str): The name of the character.
            status (dict): The status of the character.
            engine (Engine): The game engine.
            event_dispatcher (EventDispatcher): The event dispatcher.
            current_environment (Environment): The current environment.
            plugins (list): The list of plugins.
            AI_controlled (bool, optional): Indicates whether the character is AI-controlled. Defaults to False.
        """        
        self.name = name
        self.status = status
        self.engine = engine
        self.event_dispatcher = event_dispatcher
        self.current_environment = current_environment
        self.current_environment.add_character(self)
        self.possible_actions = None
        self.image = None
        self.plugins = []
        for p in plugins:
            self.add_plugin(p)
        self.get_new_actions()
        if "name" in self.status and not self.name:
            self.name = self.status["name"]
        self.message_queue = []

    def perform_action(self, action: str, *args, **kwargs) -> None:
        """
        Performs an action over the current environment. Whenever an action is performed, next possible actions are updated as the character/environment might have changed.

        Args:
            action (Action): Action to perform. 
        """
        if action in self.possible_actions:
            action_instance = self.engine.action_registry.get_action(action)
            action_instance.perform(self, self.current_environment, *args, **kwargs)
            self.get_new_actions()
            
    def get_new_actions(self) -> None:
        """
        Updates the possible actions that the character can perform in the current environment.
        """
        self.possible_actions = [action for action in self.current_environment.possible_actions if self.engine.action_registry.get_action(action).check_condition(self, self.current_environment)]

    def move_to_superior_environment(self) -> None:
        """
        Moves the character to the superior environment.
        """
        self.change_environment(self.current_environment.superior_environment)

    def change_environment(self, new_environment: 'Environment') -> None:
        """
        Changes the current environment of the character.

        Args:
            new_environment (Environment): New environment for the character.
        """
        print("NUEVO ENTORNO:", new_environment.name)
        self.current_environment.remove_character(self)
        new_environment.add_character(self)
        self.current_environment = new_environment
        self.get_new_actions()

    def destroy(self) -> None:
        """
        Destroys the character, removing it from the current environment. Python's garbage collector will remove it as it is not referenced anywhere else.
        """
        self.current_environment.remove_character(self)

    def add_plugin(self, plugin: 'Plugin') -> None:
        """
        Adds a plugin to the character.

        Args:
            plugin (Plugin): The plugin to add.
        """        
        self.plugins.append(plugin)
        plugin.initialize(self)
        self.subscribe_to_events(plugin)

    def subscribe_to_events(self, plugin: 'Plugin') -> None:
        """
        Subscribes the character to events from the plugin.

        Args:
            plugin (Plugin): The plugin to subscribe to.
        """
        if hasattr(plugin, 'get_subscriptions'):
            subscriptions = plugin.get_subscriptions()
            for event_type in subscriptions:
                self.event_dispatcher.subscribe(event_type, plugin)

    def notify_plugins(self, event_type: str, event_data: dict) -> None:
        """
        Notifies the plugins about an event.

        Args:
            event_type (str): The type of the event.
            event_data (dict): The data associated with the event.
        """
        # This method may be deprecated if the event dispatcher handles all
        self.event_dispatcher.dispatch(self, event_type, event_data)

    def add_message(self, message):
        """Add a message to the character's message queue."""
        self.message_queue.append(message)

    def display_messages(self):
        """Returns the list of messages and clears the queue."""
        messages_to_display = self.message_queue[:]
        self.message_queue = []  # Clear the message queue
        return messages_to_display