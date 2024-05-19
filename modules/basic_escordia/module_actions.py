import random
import copy
import environment as e
import character as c

def walk(actor, current_environment, new_environment):
    new_environment = actor.engine.get_environment(new_environment)
    actor.add_message(f"{actor.name} walks from {current_environment.name} to {new_environment.name}.")
    actor.change_environment(new_environment)

def walk_params(actor, current_environment):
    return [e.name for e in current_environment.contiguous_environments] 

def talk(actor, current_environment, npc):
    if npc in current_environment.status.get("npcs", []):
        actor.notify_plugins('talk_to_npc', {'npc_name': npc})

def talk_params(actor, current_environment):
    return current_environment.status.get("npcs", [])

def talk_condition(actor, current_environment) -> bool:
    return current_environment.status.get("npcs", False) 

def rest(actor, current_environment):
    actor.status["stats"]["HP"] = actor.status["stats"]["MAXHP"]
    actor.status["stats"]["MP"] = actor.status["stats"]["MAXMP"]
    actor.add_message(f"{actor.name} rests and recovers all HP and MP.")

def craft(actor, current_environment, item):
    entity = actor.engine.entity_storage.get_entity(item)
    recipe = entity.status.get("recipe", {})
    for material, required_quantity in recipe.items():
        inventory_quantity = actor.status.get("inventory", {}).get(material, 0)
        if inventory_quantity < required_quantity:
            actor.add_message(f"Cannot craft {item}. Not enough {material}.")
            return
    for material, required_quantity in recipe.items():
        actor.notify_plugins("item_used", {"item_name": material, "quantity": required_quantity})
    actor.notify_plugins("item_acquired", {"item_name": item, "quantity": 1})

def craft_params(actor, current_environment):
    return [e.name for e in actor.engine.entity_storage.get_all_entities_with_field("recipe")]

def equip(actor, current_environment, item):
    if item in actor.status.get("inventory", {}):
        item_entity = actor.engine.get_entity(item)
        actor.notify_plugins("equip_item", {"item_name": item, "item_type": item_entity.status.get("type")})
    else:
        actor.add_message(f"Cannot equip {item}. Not found in inventory.")

def equip_condition(actor, current_environment) -> bool:
    items = actor.engine.entity_storage.get_entities(actor.status.get("inventory", {}).keys())
    print(items)
    weapon_list = [e for e in items if e is not None and e.status.get("type", "") == "weapon"]
    armor_list = [e for e in items if e is not None and e.status.get("type", "") == "armor"]
    return len(weapon_list) > 0 or len(armor_list) > 0

def equip_params(actor, current_environment):
    items = actor.engine.entity_storage.get_entities(actor.status.get("inventory", {}).keys())
    weapon_list = [e for e in items if e is not None and e.status.get("type", "") == "weapon"]
    armor_list = [e for e in items if e is not None and e.status.get("type", "") == "armor"]
    return [e.name for e in weapon_list + armor_list]

def fight(actor, current_environment):
    combat = e.Environment("Combat", current_environment, [], {}, ["Attack", "Spell"])
    random_enemy = actor.engine.get_entity(random.choice(current_environment.status.get("monsters", [])))
    enemy = c.Character(random_enemy.name, copy.deepcopy(random_enemy.status), actor.engine, None, combat, [])
    actor.change_environment(combat)
    actor.notify_plugins("start_fight", {"enemy": enemy})

def attack(actor, current_environment):
    actor.notify_plugins("attack", {"current_environment": current_environment})

def spell(actor, current_environment, spell):
    target = [c for c in current_environment.current_characters if c is not actor][0]
    actor.notify_plugins("cast_spell", {"spell_name": spell, "target": target})

def spell_params(actor, current_environment):
    return actor.status.get("spellbook", [])

def spell_condition(actor, current_environment) -> bool:
    return len(actor.status.get("spellbook", [])) > 0

def buy(actor, current_environment, item):
    actor.notify_plugins("buy_item", {"item_name": item})

def buy_params(actor, current_environment):
    return current_environment.status.get("items", [])

def chop_wood(actor, current_environment):
    wood_chopped = min(random.randint(1, 3), current_environment.status.get("wood", 0))
    actor.notify_plugins("item_acquired", {"item_name": "Wood", "quantity": wood_chopped})
    current_environment.status["wood"] -= wood_chopped
    actor.add_message(f"{actor.name} chopped {wood_chopped} wood.")

def chop_wood_condition(actor, current_environment) -> bool:
    return current_environment.status.get("wood", 0) > 0

def enter_dungeon(actor, current_environment):
    actor.notify_plugins("entered_dungeon", {"dungeon_entity": actor.engine.get_entity(current_environment.status.get("dungeon"))})

def enter_shop(actor, current_environment):
    actor.notify_plugins("enter_shop", {"shop_name": current_environment.status.get("shop")})

def enter_shop_condition(actor, current_environment) -> bool:
    return current_environment.status.get("shop", False)

def drink_potion(actor, current_environment):
    actor.notify_plugins("item_used", {"item_name": "Health Potion", "quantity": 1})
    actor.status["HP"] = min(actor.status["MAXHP"], actor.status["HP"] + 10)
    actor.add_message(f"{actor.name} drinks a Health Potion and heals himself! {actor.name} now has {actor.status['HP']} HP.")

def drink_potion_condition(actor, current_environment) -> bool:
    return actor.status.get("inventory", {}).get("Health Potion", 0) > 0

def exit(actor, current_environment):
    actor.change_environment(current_environment.superior_environment)