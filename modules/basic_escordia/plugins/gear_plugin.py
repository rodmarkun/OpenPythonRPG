from plugin import Plugin

class GearPlugin(Plugin):
    def __init__(self):
        # Change this to customize the gear slots available for characters
        self.gear = {
            "weapon": None,
            "armor": None
        }

    def initialize(self, character):
        # Initialize character's gear status
        character.status['gear'] = self.gear

    def get_subscriptions(self):
        # If you need this plugin to listen to events, define those here.
        return ['equip_item']
    
    def handle_event(self, character, event_type, event_data):
        if event_type == 'equip_item':
            self.equip_item(character, event_data['item_name'], event_data['item_type'])

    def equip_item(self, character, item_name, item_type):
        """Equip an item to the specified slot if the slot exists and is empty."""
        if item_type in self.gear and self.gear[item_type] is None:
            self.gear[item_type] = item_name
            item = character.engine.get_entity(item_name)
            for stat in character.status["stats"]:
                if stat in item_name:
                    character.status["stats"][stat] += item.status["stat_change"][stat]
            character.add_message(f"{character.name} has equipped {item_name} as {item_type}.")
        else:
            self.unequip_item(character, item_name, item_type)
            character.notify_plugins("item_acquired", {"item_name": item_name, "quantity": 1})
            self.equip_item(character, item_name, item_type)

    def unequip_item(self, character, item_name, item_type):
        """Unequip an item from the specified slot."""
        if item_type in self.gear and self.gear[item_type] is not None:
            item = character.engine.get_entity(item_name)
            for stat in character.status["stats"]:
                if stat in item_name:
                    character.status["stats"][stat] -= item.status["stat_change"][stat]
            character.add_message(f"{character.name} has unequipped {self.gear[item_type]} from {item_type}.")
            self.gear[item_type] = None
        else:
            character.add_message(f"No item to unequip from {item_type}.")
