from tkinter import NO
from input_utils import get_multiline_input, get_user_choice, get_working_status, \
    get_function_property_pairs, get_other_properties
from tool_util import compile_code, get_chatgpt_response, run_scribble
from code_interaction_utils import annotate_code, produce_completion_prompt, produce_verification_prompt

def main():
    # step1: get code and all properties
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
    # step2: get completed code
    completion_prompt = produce_completion_prompt(
        code, working_status, description, purpose, pairs)
    print("completion prompt\n")
    print(completion_prompt)
    # TODO: may allow the user to change the prompt using vi
    completion_system_message = "You are an assistant for solidity code completion"
    code_completion_response = get_chatgpt_response(completion_system_message, completion_prompt)
    print("code completion response\n")
    print(code_completion_response)
    completed_code = get_multiline_input(
        ("Please enter the completed code from ChatGPT, you can also make some changes.",
         "Type 'exit' on a new line to finish."))
    # step3: compile the code
    compile_result = compile_code(completed_code)
    if not compile_result:
        user_choice = get_user_choice()
        if user_choice == 'input new code':
            new_code = get_multiline_input(
                "Please enter your new code. Type 'exit' on a new line to finish.")
            if new_code:
                completed_code = new_code
        elif user_choice != 'proceed with existing code':
            print("Invalid choice made.")
            print("Proceeding with existing code.")

    # step4: generate instrumented code
    instrumented_file = run_scribble(completed_code)
    if not instrumented_file:
        print("Failed to generate instrumented code.")
        print("Proceeding with the original code.")
        instrumented_code = completed_code
    else:
        instrumented_code = open(instrumented_file).read()
    validation_prompt = produce_verification_prompt(instrumented_code)


if __name__ == '__main__':
    main()
