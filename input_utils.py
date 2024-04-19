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

def get_working_status():
    status_completer = WordCompleter(['Complete', 'Incomplete'], ignore_case=True)
    print("Question: Is your code complete or incomplete?")

    # Ask the question
    user_choice = prompt("Enter 'Complete' or 'Incomplete': ", completer=status_completer)

    # Output the result
    print(f"You entered: {user_choice}")
    if(user_choice.lower() == 'complete'):
        return True
    else:
        return False

def get_function_property_pairs():
    # TODO: add instructions for scribble specification language
    pairs = {}
    print("Enter function and property pairs. Type 'done' when finished.")

    while True:
        # Get function name
        function_name = prompt("Function name (type 'done' to finish): ").strip()
        if function_name.lower() == 'done' or function_name == '':
            break

        # Get property for the function
        property_description = prompt(
            f"Enter property for {function_name} (leave blank if not applicable): "
        ).strip()

        # Get preconditions for the function
        preconditions = []
        while True:
            precondition = prompt(
                f"Enter a precondition for {function_name} (type 'done' to finish): "
            ).strip()
            if precondition.lower() == 'done' or precondition == '':
                break
            preconditions.append(precondition)

        # Get postconditions for the function
        postconditions = []
        while True:
            postcondition = prompt(
                f"Enter a postcondition for {function_name} (type 'done' to finish): "
            ).strip()
            if postcondition.lower() == 'done' or postcondition == '':
                break
            postconditions.append(postcondition)

        # Store the function details in a dictionary
        pairs[function_name] = {
            "property": property_description,
            "preconditions": preconditions,
            "postconditions": postconditions
        }

    # Display all function-property pairs
    print("\nFunction-Property Pairs:")
    for function, details in pairs.items():
        print(f"Function: {function}")
        print("   Property: " + details["property"])
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