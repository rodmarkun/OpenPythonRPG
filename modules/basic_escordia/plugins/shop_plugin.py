from plugin import Plugin
import environment as e

class ShopPlugin(Plugin):
    def __init__(self):
        self.current_shop_inventory = []

    def initialize(self, character):
        # Initialize shopping status, if needed
        character.status['gold'] = 10

    def get_subscriptions(self):
        # This plugin listens to 'attack' events
        return ['buy_item', 'enter_shop']

    def handle_event(self, character, event_type, event_data):
        if event_type == 'buy_item':
            self.buy_item(character, event_data['item_name'])
        elif event_type == 'enter_shop':
            self.enter_shop(character, event_data['shop_name'])

    def enter_shop(self, character, shop_name):
        shop_ent = character.engine.get_entity(shop_name)
        self.current_shop_inventory = shop_ent.status['inventory']
        shop = e.Environment(shop_name, character.current_environment, [], {"items": self.current_shop_inventory, "npcs": shop_ent.status["npcs"]}, ["Buy", "Talk", "Exit"])
        character.change_environment(shop)
        character.add_message(f"You have entered a {shop_ent.status['subtype']} shop.")
        character.add_message(f"The following items are available for purchase:\n")
        for item in self.current_shop_inventory:
            character.add_message(f"{item} - {character.engine.get_entity(item).status['value']} Gold")

    def buy_item(self, character, item_name):
        item_ent = character.engine.get_entity(item_name)
        if item_ent.status['value'] <= character.status['gold']:
            character.status['gold'] -= item_ent.status['value']
            character.notify_plugins('item_acquired', {'item_name': item_name, 'quantity': 1})
            character.add_message(f"Bought {item_name} for {item_ent.status['value']} Gold.")
        else:
            character.add_message("Not enough Gold.")


