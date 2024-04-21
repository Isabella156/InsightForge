from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import ANSI


def get_multiline_input(mutiline_prompt):
    lines = []
    print(mutiline_prompt)

    while True:
        line = prompt(ANSI('\x1b[94m>>> \x1b[0m'))
        if line == "exit":
            break
        lines.append(line)

    user_input = '\n'.join(lines)
    return user_input


def get_function_property_pairs():
    pairs = {}
    print("\x1b[94mEnter function and property pairs using scribble specification language.\x1b[0m")

    while True:
        # Get function name
        function_name = prompt(
            ANSI('\x1b[94mFunction name (leave blank if not applicable): \x1b[0m')).strip()
        if function_name == '':
            break

        # Get property for the function
        property_description = prompt(
            ANSI(
                f"\x1b[94mEnter property for {function_name} (leave blank if not applicable): \x1b[0m")
        ).strip()

        description_description = prompt(
            ANSI(
                f"\x1b[94mEnter description for {function_name} (leave blank if not applicable): \x1b[0m")
        ).strip()

        purpose_description = prompt(
            ANSI(
                f"\x1b[94mEnter purpose for {function_name} (leave blank if not applicable): \x1b[0m")
        ).strip()

        # Get preconditions for the function
        preconditions = []
        while True:
            precondition = prompt(
                ANSI(
                    f"\x1b[94mEnter a precondition for {function_name} (leave blank if not applicable): \x1b[0m")
            ).strip()
            if precondition == '':
                break
            preconditions.append(precondition)

        # Get postconditions for the function
        postconditions = []
        while True:
            postcondition = prompt(
                ANSI(
                    f"\x1b[94mEnter a postcondition for {function_name} (leave blank if not applicable): \x1b[0m")
            ).strip()
            if postcondition == '':
                break
            postconditions.append(postcondition)

        # Store the function details in a dictionary
        pairs[function_name] = {
            "property": property_description,
            "description": description_description,
            "purpose": purpose_description,
            "preconditions": preconditions,
            "postconditions": postconditions
        }

    # Display all function-property pairs
    print("\x1b[95m\nFunction-Property Pairs:\x1b[0m")
    for function, details in pairs.items():
        print(f"\x1b[95mFunction: {function}")
        print("   \x1b[95mProperty: " + details["property"] + "\x1b[0m")
        print("   \x1b[95mDescription: " + details["description"] + "\x1b[0m")
        print("   \x1b[95mPurpose: " + details["purpose"] + "\x1b[0m")
        if details["preconditions"]:
            print("   \x1b[95mPreconditions: " +
                  ", ".join(details["preconditions"]) + "\x1b[0m")
        if details["postconditions"]:
            print("   \x1b[95mPostconditions: " +
                  ", ".join(details["postconditions"]) + "\x1b[0m")

    return pairs


def get_other_properties():
    description_prompt = "\x1b[94mEnter a description for the code. Type 'exit' on a new line to finish.\x1b[0m"
    purpose_prompt = "\x1b[94mEnter the purpose of the code. Type 'exit' on a new line to finish.\x1b[0m"
    description = get_multiline_input(description_prompt)
    purpose = get_multiline_input(purpose_prompt)
    return description, purpose


def get_user_choice(choices, prompt_message):
    completer = WordCompleter(choices, ignore_case=True)
    user_choice = prompt(
        ANSI(f'\x1b[94m{prompt_message} \x1b[0m'), completer=completer)
    return user_choice.strip().lower()


def get_mythril_parameters():
    print("\x1b[94mPlease provide the fcommand line arguments parameters for Mythril",
          "command using the provided results from ChatGPT.\x1b[0m")

    defaults = {
        'transaction_depth': '1',
        'execution_timeout': '86400',
        'solver_timeout': '25000'
    }

    parameters = {}

    parameters['transaction_depth'] = prompt(
        ANSI(
            '\x1b[94mEnter transaction depth (press Enter to use the default 5): \x1b[0m'),
        default=defaults['transaction_depth'])
    parameters['execution_timeout'] = prompt(
        ANSI(
            '\x1b[94mEnter execution timeout in seconds (Press Enter to use the default 86400): \x1b[0m'),
        default=defaults['execution_timeout'])
    parameters['solver_timeout'] = prompt(
        ANSI(
            '\x1b[94mEnter solver timeout in milliseconds (Press Enter to use the default 25000): \x1b[0m'),
        default=defaults['solver_timeout'])

    print("\x1b[95mParameters Set:\x1b[0m")
    for key, value in parameters.items():
        print("\x1b[95m{:<20}: {}\x1b[0m".format(
            key.replace('_', ' ').capitalize(), value))

    return parameters
