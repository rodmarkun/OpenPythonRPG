from plugin import Plugin
import random

class SpellPlugin(Plugin):
    def initialize(self, character):
        # Initialize character's spellbook
        character.status['spellbook'] = []

    def get_subscriptions(self):
        # This plugin listens to 'learn_spell' and 'cast_spell' events
        return ['learn_spell', 'cast_spell']

    def handle_event(self, character, event_type, event_data):
        if event_type == 'learn_spell':
            self.learn_spell(character, event_data['spell_name'])
        elif event_type == 'cast_spell':
            self.cast_spell(character, event_data['spell_name'], event_data['target'])
            character.notify_plugins("spell_casted", {"current_environment": character.current_environment})

    def learn_spell(self, character, spell_name):
        # Add the spell to the character's spellbook
        character.status['spellbook'].append(spell_name)
        character.add_message(f"{character.name} has learned the spell: {spell_name}.")

    def cast_spell(self, character, spell_name, target):
        # Check if the spell is in the character's spellbook
        if spell_name in character.status['spellbook']:
            spell = character.engine.get_entity(spell_name)
            # Assuming spells can have effects like damage, healing, or utility
            if 'effect' in spell.status:
                effect_type = spell.status['effect']['type']
                magnitude = spell.status['effect']['magnitude']
                mana_cost = spell.status['mana_cost']
                # Check if the character has enough mana to cast the spell
                if character.status['stats']['MP'] < mana_cost:
                    character.add_message(f"{character.name} does not have enough mana to cast {spell_name}.")
                    return
                character.status['stats']['MP'] -= mana_cost
                character.add_message(f"{character.name} casts {spell_name}!")
                # Example effect processing
                if effect_type == 'damage':
                    self.apply_damage_effect(character, magnitude, target)
                elif effect_type == 'healing':
                    self.apply_healing_effect(character, magnitude, target)
            else:
                character.add_message(f"{character.name} casts {spell_name}, but it has no effect.")
        else:
            character.add_message(f"{character.name} tries to cast {spell_name}, but does not know it.")

    def apply_damage_effect(self, character, damage, target):
        dmg = max(0, damage - target.status["stats"]["MDEF"] // 2)
        target.status["stats"]["HP"] -= dmg
        character.add_message(f"{character.name} deals {dmg} damage.")

    def apply_healing_effect(self, character, heal_amount, target):
        # Assume some logic to heal the character
        character.add_message(f"{character.name} heals for {heal_amount} points.")
