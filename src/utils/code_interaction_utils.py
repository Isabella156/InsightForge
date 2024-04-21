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

def produce_verification_prompt(code):
    prompt = f"""
    I have a Solidity smart contract that has been instrumented for runtime verification. Below is the instrumented code:
    ```
    {code}
    ```
    I need to use the Mythril tool to validate this code and uncover any potential security vulnerabilities. However, I am unsure about the optimal settings for the following parameters:

    - Transaction count (`-t`): Specifies the number of transactions to simulate.
    - Execution timeout (`--execution-timeout`): Specifies the maximum time Mythril should spend executing the analysis, in seconds.
    - Solver timeout (`--solver-timeout`): Specifies the maximum time allowed for the solver to run, in milliseconds.

    Could you suggest the best values for these parameters to achieve thorough and effective security analysis? Also, please provide the complete Mythril command incorporating your recommended settings.
    """
    return prompt

def produce_further_action_prompt(verification_info, instructed_code):
    prompt_text = (
        "I've run a Mythril verification on a section of my smart contract,"
        " and it identified several issues. Here is the code I analyzed:"
        f"```solidity\n{instructed_code}\n```\n",
        "Here are the details of the issues found:\n",
        f"{verification_info}\n",
        "Based on the code and these findings, could you suggest some specific"
        "modifications or best practices"
    )
    return prompt_text
