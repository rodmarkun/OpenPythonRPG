import discord
import info_msgs
import emojis
import modules.basic_escordia.plugins.combat_plugin as combat_plugin
import interface_utils
from StringProgressBar import progressBar


def embed_help_msg(ctx) -> discord.Embed:
    """
    Sends embed used for !help command

    :param ctx: Discord CTX
    :return: Embed
    """
    embed = discord.Embed(
        # General info
        title=f'Escordia Help',
        description=f'{info_msgs.HELP_MSG}',
        color=discord.Colour.red()
    )
    return embed

def embed_fight_msg(ctx, player_obj, enemy) -> discord.Embed:
    """
    Sends embed used while fighting

    :param ctx: Discord CTX
    :param player_obj: Player object
    :param enemy: Enemy object
    :return: Embed
    """

    # Progress bars for HP and MP
    hp_bar = progressBar.filledBar(enemy.status['stats']['MAXHP'], enemy.status['stats']['HP'], size=10)
    player_hp_bar = progressBar.filledBar(player_obj.status['stats']['MAXHP'], player_obj.status['stats']['HP'], size=10)
    player_mp_bar = progressBar.filledBar(player_obj.status['stats']['MAXMP'], player_obj.status['stats']['MP'], size=10)

    embed = discord.Embed(
        # General info
        title=f'Fight - {ctx.author.name.capitalize()}',
        description=f'You are fighting a **{enemy.name}**.\n'
                    f'HP: {hp_bar[0]} - {enemy.status['stats']["HP"]}/{enemy.status['stats']["MAXHP"]}',
        color=discord.Colour.red()
    )
    # Images
    embed.set_thumbnail(url=enemy.image_url)
    embed.set_image(url=ctx.author.avatar.url)

    # Player stats
    embed.set_footer(
        text=f'HP: {player_obj.status['stats']["HP"]}/{player_obj.status['stats']["MAXHP"]} | {player_hp_bar[0]}\nMP: '
             f'{player_obj.status['stats']["MP"]}/{player_obj.status['stats']["MAXMP"]} | {player_mp_bar[0]}\nHit chance: '
             f'{100 - combat_plugin.miss_formula(player_obj.status['stats']["SPEED"], enemy.status['stats']["SPEED"])}% | Critical chance: '
             f'{player_obj.stats["CRITCH"]}%')

    return embed


def embed_victory_msg(ctx, msg: str) -> discord.Embed:
    """
    Sends an embed when victorious in combat

    :param ctx: Discord CTX
    :param msg: Victory message
    :return: Embed
    """

    embed = discord.Embed(
        title=f'{emojis.SPARKLER_EMOJI} Victory! {emojis.SPARKLER_EMOJI}',
        description=msg,
        color=discord.Colour.red()
    )
    embed.set_image(url=ctx.author.avatar.url)

    return embed


def embed_death_msg(ctx) -> discord.Embed:
    """
    Sends an embed when player dies

    :param ctx: Discord CTX
    :return: Embed
    """
    embed = discord.Embed(
        title=f'{emojis.SKULL_EMOJI} Death {emojis.SKULL_EMOJI}',
        description='You have died.',
        color=discord.Colour.red()
    )
    embed.set_image(url=ctx.author.avatar.url)

    return embed

def embed_player_profile(ctx, player_inst) -> discord.Embed:
    """
    Embed for whenever the player checks their profile.

    :param ctx: Discord's CTX
    :param player_inst: Player's instance
    :return: Embed
    """

    embed = discord.Embed(
        title=f'Profile - {player_inst.name.capitalize()}',
        description=interface_utils.show_player_info(player_inst),  #
        color=discord.Colour.red()
    )

    embed.add_field(name='Stats', value=interface_utils.show_player_stats(player_inst), inline=True)
    embed.add_field(name='Inventory', value=f'{player_inst.inventory.show_inventory()}', inline=True)
    embed.add_field(name='Currencies',
                    value=f'{player_inst.status['money']}G',
                    inline=True)
    embed.set_thumbnail(url=ctx.author.avatar.url)

    return embed