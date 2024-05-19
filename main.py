import character
import engine
import interfaces.console_interface as interface
from event_dispatcher import EventDispatcher
from modules.basic_escordia.plugins.inventory_plugin import InventoryPlugin
from modules.basic_escordia.plugins.dungeon_plugin import DungeonPlugin
from modules.basic_escordia.plugins.gear_plugin import GearPlugin
from modules.basic_escordia.plugins.dialogue_plugin import SimpleDialoguePlugin
from modules.basic_escordia.plugins.spell_plugin import SpellPlugin
from modules.basic_escordia.plugins.combat_plugin import CombatPlugin
from modules.basic_escordia.plugins.shop_plugin import ShopPlugin

engine = engine.Engine("modules/basic_escordia")
PLAYER_STARTING_STATUS = {"type": "player"}
chara = character.Character("Chara", PLAYER_STARTING_STATUS, engine, EventDispatcher(), engine.environments["Peaceful Village"], [InventoryPlugin(), DungeonPlugin(), GearPlugin(), SimpleDialoguePlugin(), SpellPlugin(), CombatPlugin(), ShopPlugin()])
interface.run(chara)