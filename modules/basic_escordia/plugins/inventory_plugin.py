from plugin import Plugin

class InventoryPlugin(Plugin):
    def __init__(self):
        self.items = {}  # Stores item types and their quantities

    def initialize(self, character):
        character.status['inventory'] = self.items
        self.assigned_character = character

    def get_subscriptions(self):
        return ['item_acquired', 'item_used', 'item_equipped']

    def handle_event(self, character, event_type, event_data):
        if event_type == 'item_acquired':
            self.add_item(character, event_data['item_name'], event_data['quantity'])
        elif event_type == 'item_used':
            self.use_item(character, event_data['item_name'], event_data['quantity'])
        elif event_type == 'equip_item':
            self.equip_item(character, event_data['item_name'])

    def add_item(self, character, item_name, quantity):
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity
        character.add_message(f"Added {quantity} {item_name}(s). Total now: {self.items[item_name]}.")

    def use_item(self, character, item_name, quantity):
        if item_name in self.items and self.items[item_name] >= quantity:
            self.items[item_name] -= quantity
            if self.items[item_name] == 0:
                del self.items[item_name]
        else:
            character.add_message(f"Cannot use {quantity} {item_name}(s).")

    def equip_item(self, character, item_name):
        if item_name in self.items:
            self.items[item_name] -= 1
            if self.items[item_name] == 0:
                del self.items[item_name]
