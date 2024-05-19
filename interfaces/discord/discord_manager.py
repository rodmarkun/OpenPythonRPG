import os
import discord
import discord_embeds
import discord_ui
import character
from discord.ext import commands
import engine
from event_dispatcher import EventDispatcher
from modules.basic_escordia.plugins.inventory_plugin import InventoryPlugin
from modules.basic_escordia.plugins.dungeon_plugin import DungeonPlugin
from modules.basic_escordia.plugins.gear_plugin import GearPlugin
from modules.basic_escordia.plugins.dialogue_plugin import SimpleDialoguePlugin
from modules.basic_escordia.plugins.spell_plugin import SpellPlugin
from modules.basic_escordia.plugins.combat_plugin import CombatPlugin

engine = engine.Engine("modules/basic_escordia")
PLAYER_STARTING_STATUS = {"type": "player"}

# Discord token from VENV
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

# Bot initialization
intents = discord.Intents.all()
activity = discord.Activity(type=discord.ActivityType.watching, name="!start")
bot = commands.Bot(command_prefix='!', intents=intents, activity=activity)
bot.remove_command('help')
CHARACTERS = {}

# Discord Commands
@bot.command()
async def start(ctx):
    '''
    !start command
    Creates a new character
    '''
    if ctx.author.name in CHARACTERS:
        await ctx.send("You already have a character!", embed=discord_embeds.embed_player_profile(ctx, chara), view=discord_ui.PlayerMenu(ctx, CHARACTERS[ctx.author.name]))
        return
    chara = character.Character(ctx.author.name.capitalize() , PLAYER_STARTING_STATUS, engine, EventDispatcher(), engine.environments["Peaceful Village"], [InventoryPlugin(), DungeonPlugin(), GearPlugin(), SimpleDialoguePlugin(), SpellPlugin(), CombatPlugin()])
    CHARACTERS[ctx.author.name] = chara
    await ctx.send(embed=discord_embeds.embed_player_profile(ctx, chara), view=discord_ui.PlayerMenu(ctx, chara))