import environment as e

peaceful_village = e.Environment("Peaceful Village", None, [], {'shops': ['Blacksmith_PV'], 'npcs': ['Guard', 'Wandering Mage']}, ["Talk", "Craft", "Equip", "Walk", "Rest"])
small_forest = e.Environment("Small Forest", None, [], {'wood': 50, 'monsters': ['Wolf', 'Bat']}, ["Talk", "Chop Wood", "Equip", "Fight", "Walk"])
goblin_cave = e.Environment("Goblin Cave", None, [], {'dungeon': 'Goblin Cave'}, ["Talk", "Equip","Enter Dungeon", "Walk"])

peaceful_village.add_contiguous_environment(small_forest)
small_forest.add_contiguous_environment(peaceful_village)
small_forest.add_contiguous_environment(goblin_cave)
goblin_cave.add_contiguous_environment(small_forest)
