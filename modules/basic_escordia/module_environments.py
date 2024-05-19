import environment as e

peaceful_village = e.Environment("Peaceful Village", None, [], {'shop': 'Blacksmith_PV', 'npcs': ['Guard', 'Wandering Mage']}, ["Talk", "Walk", "Craft", "Equip", "Rest", "Enter Shop"])
small_forest = e.Environment("Small Forest", None, [], {'wood': 50, 'monsters': ['Wolf', 'Bat']}, ["Talk", "Walk", "Chop Wood", "Equip", "Fight", "Enter Shop"])
goblin_cave = e.Environment("Goblin Cave", None, [], {'dungeon': 'Goblin Cave'}, ["Talk", "Walk", "Equip","Enter Dungeon", "Enter Shop"])

peaceful_village.add_contiguous_environment(small_forest)
small_forest.add_contiguous_environment(peaceful_village)
small_forest.add_contiguous_environment(goblin_cave)
goblin_cave.add_contiguous_environment(small_forest)
