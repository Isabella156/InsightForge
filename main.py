from random import choice

from code_interaction_utils import (annotate_code, produce_completion_prompt,
                                    produce_further_action_prompt,
                                    produce_verification_prompt)
from input_utils import (get_function_property_pairs, get_multiline_input,
                         get_mythril_parameters, get_other_properties,
                         get_user_choice)
from tool_util import (compile_code, get_chatgpt_response, run_mythril,
                       run_scribble)


def main():
    # step1: get code and all properties
    code_prompt = "Please enter your code. Type 'exit' on a new line to finish."
    code = get_multiline_input(code_prompt)
    print("code\n")
    print(code)
    working_status_choices = ['Complete', 'Incomplete']
    working_status_prompt = ("Is your code complete or incomplete?"
                             "Enter 'Complete' or 'Incomplete': ")
    working_status = get_user_choice(
        working_status_choices, working_status_prompt)
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
    completion_system_message = "You are an assistant for solidity code completion"
    code_completion_response = get_chatgpt_response(
        completion_system_message, completion_prompt)
    print("code completion response\n")
    print(code_completion_response)
    completed_code = get_multiline_input(
        ("Please enter the completed code from ChatGPT, you can also make some changes."
         "Type 'exit' on a new line to finish."))
    # step3: compile the code
    compile_result = compile_code(completed_code)
    if not compile_result:
        code_completion_choice = [
            'proceed with existing code', 'input new code']
        code_completion_prompt = ("Do you want to proceed with the existing code or"
                                  "input a new code?")
        user_choice = get_user_choice(
            code_completion_choice, code_completion_prompt)
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
        instrumented_file = "original.flat.sol"
        open(instrumented_file, 'w').write(instrumented_code)
    else:
        instrumented_code = open(instrumented_file).read()
    # step5: get verification command
    verification_prompt = produce_verification_prompt(instrumented_code)
    print("verification prompt\n")
    print(verification_prompt)
    verification_system_message = ("You are an assistant for providing mythril"
                                   "verification commands according to the code")
    verification_response = get_chatgpt_response(
        verification_system_message, verification_prompt)
    print("verification response\n")
    print(verification_response)
    parameters = get_mythril_parameters()
    # step6: get verification results
    mythril_sucess, mythril_results = run_mythril(
        instrumented_file, parameters)
    goodbye_message = "InsightForge has completed the task.\nThank you for using it :)"
    if mythril_sucess is True:
        print("Mythril verification successful.")
        print(goodbye_message)
        return
    elif mythril_sucess is False:
        print("Mythril verification failed.")
        further_action_choices = ['Exit the program',
                                  'Get further verification instructions from ChatGPT']
        further_action_prompt = ("Do you want to exit the program or"
                                 "get further verification instructions from ChatGPT?")
        further_action_choice = get_user_choice(
            further_action_choices, further_action_prompt)
        if further_action_choice == 'Exit the program':
            print("InsightForge has completed the task.")
            print(goodbye_message)
            return
        elif further_action_choice == 'Get further verification instructions from ChatGPT':
            print(mythril_results)
            mythril_results_info = get_multiline_input(("Please enter the valuable"
                                                        "information from Mythril verification results used for ChatGPT."))
            further_action_prompt = produce_further_action_prompt(
                mythril_results_info, instrumented_code)
            print("further action prompt\n")
            print(further_action_prompt)
            further_action_system_message = ("You are an assistant for suggesting further actions"
                                             "after mythril verification failed")
            further_action_response = get_chatgpt_response(
                further_action_system_message, further_action_prompt)
            print("further action response\n")
            print(further_action_response)
            print("Please take further action based on the response.")
            print(goodbye_message)
    else:
        print("Mythril verification failed.")
        print(goodbye_message)
        return


if __name__ == '__main__':
    main()
