from plugin import Plugin
import environment as e
import character as c
import random
import copy

class DungeonPlugin(Plugin):
    def __init__(self):
        self.dungeon_name = None
        self.original_enemy_count = 0
        self.current_enemy_count = 0
        self.possible_enemies = []
        self.boss = None

    def initialize(self, character):
        # Initially, there is no dungeon data until the character enters a dungeon.
        pass

    def get_subscriptions(self):
        return ['entered_dungeon', 'enemy_defeated_in_dungeon', 'player_died', 'defeated_boss']

    def handle_event(self, character, event_type, event_data):
        if event_type == 'entered_dungeon':
            self.setup_dungeon(character, event_data)
        elif event_type == 'enemy_defeated_in_dungeon' and character.status['in_dungeon']:
            self.enemy_defeated(character, event_data)
        elif event_type == 'player_died' and character.status['in_dungeon']:
            self.reset_dungeon(character)
        elif event_type == 'defeated_boss' and character.status['in_dungeon']:
            character.add_message(f"Defeated the boss of the dungeon: {self.dungeon_name}.")
            character.status['in_dungeon'] = False

    def setup_dungeon(self, character, event_data):
        dungeon_entity = event_data['dungeon_entity']
        self.dungeon_name = dungeon_entity.name
        self.dungeon_entity = dungeon_entity
        self.original_enemy_count = self.dungeon_entity.status['number_of_enemies']
        self.current_enemy_count = self.dungeon_entity.status['number_of_enemies']
        self.possible_enemies = self.dungeon_entity.status['monsters']
        self.boss = self.dungeon_entity.status['boss']
        character.status['in_dungeon'] = True
        character.add_message(f"Entered the dungeon: {self.dungeon_name} with {self.current_enemy_count} enemies.")
        self.fight_enemy_dungeon(character)

    def enemy_defeated(self, character, event_data):
        if event_data['monster_name'] in self.possible_enemies:
            self.current_enemy_count -= 1
            character.add_message(f"Defeated {event_data['monster_name']}, {self.current_enemy_count} enemies left.")
            if self.current_enemy_count == 0:
                self.initiate_boss_fight(character)
            else:
                self.fight_enemy_dungeon(character)

    def reset_dungeon(self, character):
        self.current_enemy_count = self.original_enemy_count
        character.status['in_dungeon'] = False
        character.add_message(f"Player died, resetting dungeon.")

    def initiate_boss_fight(self, character):
        character.add_message(f"All enemies defeated. Time to fight the boss: {self.dungeon_entity.status['boss']}")
        self.fight_enemy_dungeon(character, self.boss)

    def fight_enemy_dungeon(self, character, enemy=None):
        combat = e.Environment("Combat", character.current_environment, [], {}, ["Attack", "Spell"])
        if enemy is None:
            selected_enemy = character.engine.get_entity(random.choice(self.possible_enemies))
        else:
            selected_enemy = character.engine.get_entity(enemy)
        enemy = c.Character(selected_enemy.name, copy.deepcopy(selected_enemy.status), character.engine, None, combat, [])
        character.change_environment(combat)
        character.notify_plugins("start_fight", {"enemy": enemy})
