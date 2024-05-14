import shlex  # A module for parsing shell-like syntaxes
import modules.basic_escordia.module_actions as module_actions

def generate_status_bar(current, maximum, color_code):
    """ Generate a colored bar indicating the current status in 10 sectors, where each sector represents 10% of the maximum value """
    percentage = (current / maximum) * 100
    filled_sectors = int(percentage // 10)
    empty_sectors = 10 - filled_sectors
    # Using ANSI escape codes to color the bar
    return f"\033[{color_code}m" + '■' * filled_sectors + ' ' * empty_sectors + "\033[0m"

def display_interface(character, actions, environment):
    print("\n" + "="*60)
    print(f"Character Status: {character.name}")
    print("-"*60)
    
    # Display character details
    print(f"Type: {character.status['type']}, XP: {character.status['xp']}, Level: {character.status['lvl']}")
    print(f"XP to Next Level: {character.status['xptonextlvl']}")
    print("Stats:")
    for stat, value in character.status['stats'].items():
        print(f"  {stat}: {value}")

    # Display HP and MP with graphical colored bars
    # 31 for red, 34 for blue
    print(f"HP: {generate_status_bar(character.status['stats']['HP'], character.status['stats']['MAXHP'], '31')}")
    print(f"MP: {generate_status_bar(character.status['stats']['MP'], character.status['stats']['MAXMP'], '34')}")
    
    print("Gear:")
    for gear_type, gear_item in character.status['gear'].items():
        print(f"  {gear_type.capitalize()}: {gear_item if gear_item else 'None'}")
    
    # Display spellbook if it exists in the character's status
    if 'spellbook' in character.status:
        print("Spellbook:")
        for spell in character.status['spellbook']:
            print(f"  {spell}")

    print("Inventory:")
    if character.status['inventory']:
        for item, quantity in character.status['inventory'].items():
            print(f"  {item}: {quantity}")
    else:
        print("  Empty")

    # Display environment details
    print("\nCurrent Environment: " + environment.name)
    print("Contiguous Environments: " + ", ".join([e.name for e in environment.contiguous_environments]))
    print("Env Status:")
    for key, value in environment.status.items():
        if isinstance(value, list):
            print(f"  {key.capitalize()}: {', '.join(value)}")
    
    print("="*60)

    print("\n")
    print("\n -> ".join(character.display_messages()))
    print("\n")



def parse_input(prompt, options):
    """ Parse numeric input and map it to provided options. """
    try:
        selected_index = int(input(prompt)) - 1
        if selected_index >= 0 and selected_index < len(options):
            return options[selected_index]
        else:
            raise ValueError("Selected index is out of range.")
    except ValueError as e:
        print(f"Input error: {e}")
        return None


def run(actor):

    while True:
        display_interface(actor, actor.possible_actions, actor.current_environment)
        available_actions = [a for a in actor.possible_actions]
        # Display actions with numbers
        for i, action in enumerate(available_actions, start=1):
            print(f"{i}. {action}")

        # User selects action by number
        selected_action = parse_input("Choose an action by number: ", available_actions)
        if selected_action:
            action_function = getattr(module_actions, f"{selected_action.lower().replace(' ', '_')}", None)
            
            # Get parameters if the action function requires them (assumes there's a corresponding _params function if needed)
            params_function = getattr(module_actions, f"{selected_action.lower().replace(' ', '_')}_params", None)
            if callable(params_function):
                possible_params = params_function(actor, actor.current_environment)
                for i, param in enumerate(possible_params, start=1):
                    print(f"{i}. {param}")
                selected_param = parse_input("Choose a parameter by number: ", possible_params)
                if selected_param:
                    action_function(actor, actor.current_environment, selected_param)
            else:
                action_function(actor, actor.current_environment)
        else:
            print("Invalid action, please try again.")
