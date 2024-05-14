from plugin import Plugin

class SimpleDialoguePlugin(Plugin):
    def initialize(self, character):
        # Initialize dialogue status to track which NPCs have been spoken to
        character.status['dialogues'] = {}

    def get_subscriptions(self):
        # This plugin listens to 'talk_to_npc' events, which should be triggered by the game logic
        return ['talk_to_npc']

    def handle_event(self, character, event_type, event_data):
        if event_type == 'talk_to_npc':
            self.process_dialogue(character, event_data['npc_name'])

    def process_dialogue(self, character, npc_name):
        npc = character.engine.get_entity(npc_name)
        if npc_name not in character.status['dialogues']:
            character.add_message(f"{npc_name}: {npc.status['dialogue']}")
            character.status['dialogues'][npc_name] = True
            if npc.status.get('triggers', False):
                for key, value in npc.status['triggers'].items():
                    character.notify_plugins(key, value)
        else:
            character.add_message(f"{npc_name}: {npc.status['exhausted_dialogue']}")
