from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

def get_multiline_input(mutiline_prompt):
    lines = []
    print(mutiline_prompt)

    while True:
        line = prompt('>>> ')
        if line == "exit":
            break
        lines.append(line)

    user_input = '\n'.join(lines)

    # print("You entered:")
    # print(user_input)

    return user_input

# TODO: merge this function with get user choice
def get_working_status():
    status_completer = WordCompleter(['Complete', 'Incomplete'], ignore_case=True)
    print("Question: Is your code complete or incomplete?")

    # Ask the question
    user_choice = prompt("Enter 'Complete' or 'Incomplete': ", completer=status_completer)

    # Output the result
    print(f"You entered: {user_choice}")
    return user_choice

def get_function_property_pairs():
    # TODO: add instructions for scribble specification language
    pairs = {}
    print("Enter function and property pairs.")

    while True:
        # Get function name
        function_name = prompt("Function name (leave blank if not applicable): ").strip()
        if function_name == '':
            break

        # Get property for the function
        property_description = prompt(
            f"Enter property for {function_name} (leave blank if not applicable): "
        ).strip()

        description_description = prompt(
            f"Enter description for {function_name} (leave blank if not applicable): "
        ).strip()

        purpose_description = prompt(
            f"Enter purpose for {function_name} (leave blank if not applicable): "
        ).strip()

        # Get preconditions for the function
        preconditions = []
        while True:
            precondition = prompt(
                f"Enter a precondition for {function_name} (leave blank if not applicable): "
            ).strip()
            if precondition == '':
                break
            preconditions.append(precondition)

        # Get postconditions for the function
        postconditions = []
        while True:
            postcondition = prompt(
                f"Enter a postcondition for {function_name} (leave blank if not applicable): "
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
    print("\nFunction-Property Pairs:")
    for function, details in pairs.items():
        print(f"Function: {function}")
        print("   Property: " + details["property"])
        print("   Description: " + details["description"])
        print("   Purpose: " + details["purpose"])
        if details["preconditions"]:
            print("   Preconditions: " + ", ".join(details["preconditions"]))
        if details["postconditions"]:
            print("   Postconditions: " + ", ".join(details["postconditions"]))
        print()

    return pairs

def get_other_properties():
    description_prompt = "Enter a description for the code: "
    purpose_prompt = "Enter the purpose of the code: "
    description = get_multiline_input(description_prompt)
    purpose = get_multiline_input(purpose_prompt)
    return description, purpose

def get_user_choice():
    choices = ['Proceed with existing code', 'Input new code']
    completer = WordCompleter(choices, ignore_case=True)
    user_choice = prompt('Choose an option: ', completer=completer)
    return user_choice.strip().lower()

def get_mythril_parameters():
    print("Please provide the fcommand line arguments parameters for Mythril",
          "command using the provided results from ChatGPT.")

    defaults = {
        'transaction_depth': '1',
        'execution_timeout': '86400',
        'solver_timeout': '25000'
    }

    parameters = {}

    parameters['transaction_depth'] = prompt(
        'Enter transaction depth (press Enter to use the default 5): ',
        default=defaults['transaction_depth'])
    parameters['execution_timeout'] = prompt(
        'Enter execution timeout in seconds (Press Enter to use the default 86400): ',
        default=defaults['execution_timeout'])
    parameters['solver_timeout'] = prompt(
        'Enter solver timeout in milliseconds (Press Enter to use the default 25000): ',
        default=defaults['solver_timeout'])

    return parameters
