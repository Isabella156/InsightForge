from input_utils import get_multiline_input, get_working_status, \
    get_function_property_pairs, get_other_properties

def annotate_code(code, pairs):
    lines = code.split('\n')
    for function, property in pairs.items():

        docstring = f"/// {property}\n"
        for i, line in enumerate(lines):
            # assumption: the function declaration is on a single line
            if f"function {function}(" in line:
                lines.insert(i, docstring)
                break
    return '\n'.join(lines)

def code_completion_prompt():
    prompt = "Prompt for Code Completion and Verification\n\n"
    prompt += "### Code\n" + code + "\n\n"
    prompt += "### Status: " + status + "\n\n"
    prompt += "### Contract Description\n" + description + "\n\n"
    prompt += "### Purpose\n" + purpose + "\n\n"
    prompt += "### Preconditions\n" + '\n'.join(f"- {cond}" for cond in preconditions) + "\n\n"
    prompt += "### Postconditions\n" + '\n'.join(f"- {cond}" for cond in postconditions) + "\n\n"
    prompt += "### Function-Property Pairs\n"

    for i, (function, properties) in enumerate(function_property_pairs.items(), 1):
        prompt += f"{i}. Function: `{function}`\n"
        prompt += "   - Property: " + properties.get('property', '') + "\n"
        if properties.get('preconditions'):
            prompt += "   - Preconditions: " + properties['preconditions'] + "\n"
        if properties.get('postconditions'):
            prompt += "   - Postconditions: " + properties['postconditions'] + "\n"
        prompt += "\n"

    prompt += "### Task\n"
    prompt += "Please complete the provided code snippet by ensuring all functions adhere to their specified properties and the overall contract conditions. "
    prompt += "Ensure the code is syntactically correct, adheres to the ERC20 standard, and incorporates best security practices. "
    prompt += "Highlight any additions or changes made for clarity.\n"

    return prompt

def main():
    # code_prompt = "Please enter your code. Type 'exit' on a new line to finish."
    # code = get_multiline_input(code_prompt)
    # print("code\n")
    # print(code)
    # working_status = get_working_status()
    pairs = get_function_property_pairs()
    # annotated_code = annotate_code(code, pairs)
    # print("annotated code\n")
    # print(annotated_code)
    # description, purpose, precondition, postcondition = get_other_properties()


    # code_completion_prompt()

if __name__ == '__main__':
    main()
