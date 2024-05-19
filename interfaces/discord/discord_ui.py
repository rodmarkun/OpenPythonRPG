import discord


class ActionMenu(discord.ui.View):
    """
    Class that handles the menu while in combat.
    """

    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.value = None
        self.ctx = ctx

    # Normal Attack
    @discord.ui.button(label="Attack", style=discord.ButtonStyle.red)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed(self.ctx, interaction):
            # TODO - Attack
            await interaction.response.defer()

    # Skill
    @discord.ui.button(label="Spell", style=discord.ButtonStyle.primary)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await check_button_pressed(self.ctx, interaction):
            # TODO - Spells
            await interaction.response.defer()

class PlayerMenu(discord.ui.View):
    def __init__(self, ctx, player):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.player = player
        self.create_action_buttons()

    def create_action_buttons(self):
        # Diccionario de funciones para manejar cada acción
        action_handlers = {
            "fight": self.handle_fight,
            "walk": self.handle_trade,
            "talk": self.handle_explore
        }
        
        for action in self.player.actions:
            # Crear un botón para cada acción posible
            button = discord.ui.Button(label=action.capitalize(), style=discord.ButtonStyle.blurple)
            button.callback = action_handlers.get(action, self.default_handler)
            self.add_item(button)

    async def handle_fight(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Manejador para la acción de pelea
        await interaction.response.send_message("Initiating a fight!")
        # Aquí puedes añadir más lógica relacionada con la pelea

    async def handle_trade(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Manejador para la acción de comercio
        await interaction.response.send_message("Opening trade window!")
        # Más lógica de comercio

    async def handle_explore(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Manejador para explorar
        await interaction.response.send_message("Let's explore the area!")
        # Añadir lógica de exploración

    async def default_handler(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Manejador predeterminado si la acción no está definida
        await interaction.response.send_message("This action is not implemented yet.")
        


class EntitySelect(discord.ui.Select):
    """
    Class that handles the item selection for the shop.
    """

    def __init__(self, ctx, entity_names, character, action, placeholder):
        items_in_options = entity_names
        stat_str_remove = "'"
        options = [discord.SelectOption(label=i) for i in items_in_options]
        super().__init__(placeholder=f"{placeholder}", max_values=1, min_values=1, options=options)
        self.ctx = ctx
        self.character = character
        self.action = action

    # Buys an item
    async def callback(self, interaction: discord.Interaction) -> None:
        """
        Callback function for the item selection.

        :param interaction: Discord interaction
        :return: None
        """

        if await check_button_pressed(self.ctx, interaction):
            self.character.perform_action(self.action, self.character.current_environment, self.values[0])


class EntitySelectView(discord.ui.View):
    def __init__(self, ctx, entity_names, character, action, placeholder):
        super().__init__(timeout=None)
        self.add_item(EntitySelect(ctx, entity_names, character, action, placeholder))


async def check_button_pressed(ctx, interaction: discord.Interaction) -> bool:
    """
    Checks if button has been pressed by same user that initiated the interaction.

    :param ctx: Discord's CTX
    :param interaction: Discord's interaction
    :return: True if button pressed by correspondent user, False if not. Also spits a message.
    """

    if interaction.user.name == ctx.author.name:
        return True
    else:
        await interaction.response.send_message(f"That button is not for you, {interaction.user.mention}!")
        return False


async def check_button_pressed_by_certain_name(ctx, interaction: discord.Interaction, certain_name: str) -> bool:
    """
    Checks if button has been pressed by a certain user.

    :param ctx: Discord's CTX
    :param interaction: Discord's interaction
    :param certain_name: Name of the user that should press the button
    :return: True if button pressed by correspondent user, False if not. Also spits a message.
    """

    if interaction.user.name == certain_name:
        return True
    else:
        await interaction.response.send_message(f"That button is not for you, {interaction.user.mention}!")
        return False