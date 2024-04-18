from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

def get_code_input():
    lines = []
    print("Please enter your code. Type 'exit' on a new line to finish.")

    while True:
        line = prompt('>>> ')
        if line == "exit":
            break
        lines.append(line)

    user_input = '\n'.join(lines)

    print("You entered:")
    print(user_input)

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

def get_property():
    # if_succeeds {:msg "Transfer does not modify the sum of balances" } old(_balances[_to]) +
    # old(_balances[msg.sender]) == _balances[_to] + _balances[msg.sender];
    pairs = {}
    print("Enter function and property pairs. Type 'done' when finished.")

    while True:
        # Get function name
        function_name = prompt("Function name (type 'done' to finish): ").strip()
        if function_name.lower() == 'done' or function_name == '':
            break

        # Get property for the function
        property_description = prompt(f"Enter property for {function_name}: ").strip()

        # Ensure property is not empty
        if property_description:
            # Store the pair in a dictionary
            pairs[function_name] = property_description
        else:
            print("Empty property is not allowed. Please enter a valid property.")

    # Display all function-property pairs
    print("\nFunction-Property Pairs:")
    for function, property in pairs.items():
        print(f"Function: {function}\nProperty: {property}\n")

    return pairs

def code_completion_prompt():

def main():
    # code = get_code_input()
    # working_status = get_working_status()
    # pair = get_property()

    code_completion_prompt()

if __name__ == '__main__':
    main()
