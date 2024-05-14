import random
from plugin import Plugin

class CombatPlugin(Plugin):

    def initialize(self, character):
        character.status["in_fight"] = False
        self.enemy = None
        character.status["xp"] = 0
        character.status["lvl"] = 1
        character.status["xptonextlvl"] = 5
        character.status["stats"] = {"MAXHP": 25, "HP": 25, "DEF": 5, "ATK": 10, "MAXMP": 10, "MP": 10}

    def get_subscriptions(self):
        return ['attack', 'start_fight', 'spell_casted', 'player_died']

    def handle_event(self, character, event_type, event_data):
        if event_type == 'attack':
            self.attack(character, event_data['current_environment'])
        elif event_type == "start_fight":
            self.start_fight(character, event_data["enemy"])
        elif event_type == "spell_casted":
            self.spell_casted(character, event_data["current_environment"])
        elif event_type == "player_died":
            self.player_died(character, event_data["current_environment"])
        

    def attack(self, actor, current_environment):
        actor.add_message(f"{actor.name} attacks {self.enemy.name}!")
        dmg = max(0, actor.status["stats"]["ATK"] - self.enemy.status["stats"]["DEF"] // 2)
        self.enemy.status["stats"]["HP"] -= dmg
        actor.add_message(f"{self.enemy.name} takes {dmg} damage.")
        if self.enemy.status["stats"]["HP"] <= 0:
            self.handle_victory(actor, self.enemy, current_environment)
        else:
            self.counter_attack(self.enemy, actor, current_environment)

    def spell_casted(self, actor, current_environment):
        if self.enemy.status["stats"]["HP"] <= 0:
            self.handle_victory(actor, self.enemy, current_environment)
        else:
            self.counter_attack(self.enemy, actor, current_environment)

    def start_fight(self, actor, enemy):
        self.enemy = enemy
        actor.add_message(f"{actor.name} enters combat with {enemy.name}!")
        actor.status["in_fight"] = True

    def handle_victory(self, actor, c, current_environment):
        self.enemy = None
        actor.add_message(f"{c.name} has been defeated!")
        actor.move_to_superior_environment()
        current_environment.destroy()
        actor.status["in_fight"] = False
        if c.status.get("type") in ["monster", "boss"] and c.status.get("drops", False):
            item_acquired = random.choice(c.status.get("drops"))
            actor.notify_plugins("item_acquired", {"item_name": item_acquired, "quantity": 1})
        if actor.status.get("in_dungeon", False):
            self.notify_dungeon_events(actor, c)

    def notify_dungeon_events(self, actor, c):
        if c.status.get("type") == "boss":
            actor.notify_plugins("defeated_boss", {})
        else:
            actor.notify_plugins("enemy_defeated_in_dungeon", {"monster_name": c.name})

    def counter_attack(self, c, actor, current_environment):
        actor.add_message(f"{c.name} attacks back!")
        dmg = max(0, c.status["stats"]["ATK"] - actor.status["stats"]["DEF"] // 2)
        actor.status["stats"]["HP"] -= dmg
        actor.add_message(f"{actor.name} takes {dmg} damage.")
        if actor.status["stats"]["HP"] <= 0:
            actor.notify_plugins("player_died", {"current_environment": current_environment})

    def player_died(self, actor, current_environment):
        actor.add_message(f"{actor.name} has been defeated!")
        actor.change_environment(actor.engine.environments["Peaceful Village"])
        current_environment.destroy()
        actor.status["in_fight"] = False
        actor.status["stats"]["HP"] = actor.status["stats"]["MAXHP"]
        actor.status["stats"]["MP"] = actor.status["stats"]["MAXMP"]
        self.enemy = None
