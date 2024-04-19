from input_utils import get_multiline_input, get_working_status, \
    get_function_property_pairs, get_other_properties

from openai import OpenAI

from solcx import compile_standard, install_solc, get_installed_solc_versions, set_solc_version

from solcx.exceptions import SolcError

import json
install_solc('v0.6.0')

def annotate_code(code, pairs):
    lines = code.split('\n')
    for function, details in pairs.items():
        property_description = details.get('property', '').strip()
        if property_description:
            docstring = f"/// {property_description}\n"
            for i, line in enumerate(lines):
                if f"function {function}(" in line:
                    lines.insert(i, docstring)
                    break

    return '\n'.join(lines)

def produce_completion_prompt(code, status, description, purpose, function_property_pairs):
    prompt = "Code Completion and Verification\n\n"
    prompt += "### Code\n" + code + "\n\n"
    prompt += "### Status: " + status + "\n\n"
    prompt += "### Contract Description\n" + description + "\n\n"
    prompt += "### Purpose\n" + purpose + "\n\n"
    prompt += "### Function-Property Pairs\n"

    for i, (function, properties) in enumerate(function_property_pairs.items(), 1):
        prompt += f"{i}. Function: `{function}`\n"
        prompt += "   - Description: " + properties.get('description', '') + "\n"
        prompt += "   - Purpose: " + properties.get('purpose', '') + "\n"

        # Handle preconditions if they exist and are in list format
        if properties.get('preconditions'):
            prompt += "   - Preconditions: " + "; ".join(properties['preconditions']) + "\n"

        # Handle postconditions if they exist and are in list format
        if properties.get('postconditions'):
            prompt += "   - Postconditions: " + "; ".join(properties['postconditions']) + "\n"

        prompt += "\n"

    prompt += "### Task\n"
    prompt += "Please complete the provided code snippet by ensuring all functions adhere to their specified properties and the overall contract conditions. "
    prompt += "Ensure the code is syntactically correct, adheres to the ERC20 standard, and incorporates best security practices. "
    # prompt += "Highlight any additions or changes made for clarity.\n"

    return prompt

def get_code_completion():
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
    ]
    )

    print(completion.choices[0].message)

def compile_code(code):
    # Specify the version of the compiler you need
    solc_version = '0.6.0'

    # Check if the specified version is already installed
    if solc_version not in get_installed_solc_versions():
        print(f"Installing solc version {solc_version}...")
        install_solc(solc_version)

    # Explicitly set the solc version for py-solc-x to use
    set_solc_version(solc_version)

    compiled_input = {
        "language": "Solidity",
        "sources": {
            "YourContract.sol": {"content": code}
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        }
    }

    try:
        compiled_code = compile_standard(compiled_input)
        print("Compilation successful.")
        print(json.dumps(compiled_code, indent=4))
        return compiled_code
    except SolcError as e:
        print("Compilation failed with errors:")
        print(e)
        return None


def main():
    code_prompt = "Please enter your code. Type 'exit' on a new line to finish."
    code = get_multiline_input(code_prompt)
    print("code\n")
    print(code)
    working_status = get_working_status()
    pairs = get_function_property_pairs()
    annotated_code = annotate_code(code, pairs)
    print("annotated code\n")
    print(annotated_code)
    description, purpose = get_other_properties()

if __name__ == '__main__':
    main()
