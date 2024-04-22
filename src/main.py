from utils.code_interaction_utils import (
    annotate_code,
    produce_completion_prompt,
    produce_further_action_prompt,
    produce_verification_prompt,
)
from utils.input_utils import (
    get_function_property_pairs,
    get_multiline_input,
    get_mythril_parameters,
    get_other_properties,
    get_user_choice,
)
from utils.tool_utils import compile_code, get_chatgpt_response, run_mythril, run_scribble


def get_code_and_properties():
    code_prompt = "\x1b[94mPlease enter your code. Type 'exit' on a new line to finish.\x1b[0m"
    code = get_multiline_input(code_prompt)
    print("\x1b[95mcode:\x1b[0m")
    print("\x1b[95m{}\x1b[0m".format(code))

    working_status_choices = ['Complete', 'Incomplete']
    working_status_prompt = ("Is your code complete or incomplete? "
                             "Enter 'Complete' or 'Incomplete': ")
    working_status = get_user_choice(
        working_status_choices, working_status_prompt)
    print("\x1b[95mworking status:\x1b[0m")
    print("\x1b[95m{}\x1b[0m".format(working_status))

    pairs = get_function_property_pairs()

    description, purpose = get_other_properties()
    print("\x1b[95mdescription:\x1b[0m")
    print("\x1b[95m{}\x1b[0m".format(description))
    print("\x1b[95mpurpose:\x1b[0m")
    print("\x1b[95m{}\x1b[0m".format(purpose))

    annotated_code = annotate_code(code, pairs)
    print("\x1b[95mannotated code\n\x1b[0m")
    print("\x1b[95m{}\x1b[0m".format(annotated_code))

    return annotated_code, working_status, pairs, description, purpose


def get_completed_code(code, working_status, description, purpose, pairs):
    completion_prompt = produce_completion_prompt(
        code, working_status, description, purpose, pairs)
    print("\x1b[95mcompletion prompt:\n\x1b[0m")
    print("\x1b[95m{}\x1b[0m".format(completion_prompt))

    completion_system_message = "You are an assistant for solidity code completion"
    code_completion_response = get_chatgpt_response(
        completion_system_message, completion_prompt)
    print("code completion response\n")
    print("\x1b[95m{}\x1b[0m".format(code_completion_response))

    completed_code = get_multiline_input(
        ("\x1b[94mPlease enter the completed code from ChatGPT, you can also make some changes."
         "Type 'exit' on a new line to finish.\x1b[0m"))
    print("\x1b[95mcompleted code:\n\x1b[0m")
    print("\x1b[95m{}\x1b[0m".format(completed_code))
    return completed_code


def get_compilation_results(completed_code):
    compile_result = compile_code(completed_code)
    if not compile_result:
        code_completion_choice = [
            'proceed with existing code', 'input new code']
        code_completion_prompt = ("\x1b[94mDo you want to proceed with the existing code or"
                                  "input a new code?\x1b[0m")
        user_choice = get_user_choice(
            code_completion_choice, code_completion_prompt)
        if user_choice == 'input new code':
            new_code = get_multiline_input(
                "\x1b[94mPlease enter your new code. Type 'exit' on a new line to finish.\x1b[0m")
            if new_code:
                completed_code = new_code
        elif user_choice != 'proceed with existing code':
            print("\x1b[91mInvalid choice made.\x1b[0m")
            print("\x1b[94mProceeding with existing code.\x1b[0m")
    return completed_code


def get_instrumented_code(completed_code):
    instrumented_file = run_scribble(completed_code)
    if not instrumented_file:
        print("Failed to generate instrumented code.")
        print("Proceeding with the original code.")
        instrumented_code = completed_code
        instrumented_file = "original.flat.sol"
        open(instrumented_file, 'w').write(instrumented_code)
    else:
        instrumented_code = open(instrumented_file).read()
    return instrumented_code, instrumented_file


def get_verification_results(instrumented_code, instrumented_file):
    verification_prompt = produce_verification_prompt(instrumented_code)
    print("\x1b[95mverification prompt\n\x1b[0m")
    print("\x1b[95m{}\x1b[0m".format(verification_prompt))

    verification_system_message = ("You are an assistant for providing mythril"
                                   "verification commands according to the code")
    verification_response = get_chatgpt_response(
        verification_system_message, verification_prompt)
    print("\x1b[95mverification instruction response\n\x1b[0m")
    print("\x1b[95m{}\x1b[0m".format(verification_response))

    parameters = get_mythril_parameters()
    mythril_sucess, mythril_results = run_mythril(
        instrumented_file, parameters)
    return mythril_sucess, mythril_results


def further_action(mythril_sucess, mythril_results, instrumented_code):
    goodbye_message = "\x1b[95mInsightForge has completed the task.\nThank you for using it :)\x1b[0m"
    if mythril_sucess is True:
        print("\x1b[95mMythril verification successful.\x1b[0m")
        print(goodbye_message)
        return
    elif mythril_sucess is False:
        print("\x1b[91mMythril verification failed.\x1b[0m")
        further_action_choices = ['Exit the program',
                                  'Get further verification instructions from ChatGPT']
        further_action_prompt = ("Do you want to exit the program or"
                                 "get further verification instructions from ChatGPT?")
        further_action_choice = get_user_choice(
            further_action_choices, further_action_prompt)

        if further_action_choice == 'Exit the program':
            print(goodbye_message)
            return

        elif further_action_choice == 'Get further verification instructions from ChatGPT':
            print("x1b[95m{}\x1b[0m".format(mythril_results))
            mythril_results_info = get_multiline_input(("x1b[94mPlease enter the valuable"
                                                        "information from Mythril verification results used for ChatGPT.x1b[0m"))
            print("x1b[95mmythril results info\nx1b[0m")
            print("x1b[95m{}\x1b[0m".format(mythril_results_info))

            further_action_prompt = produce_further_action_prompt(
                mythril_results_info, instrumented_code)
            print("\x1b[95mfurther action prompt\n\x1b[0m")
            print("\x1b[95m{}\x1b[0m".format(further_action_prompt))

            further_action_system_message = ("You are an assistant for suggesting further actions"
                                             "after mythril verification failed")
            further_action_response = get_chatgpt_response(
                further_action_system_message, further_action_prompt)
            print("\x1b[95mfurther action response\n\x1b[0m")
            print("\x1b[95m{}\x1b[0m".format(further_action_response))

            print(
                "\x1b[95mPlease take further action based on the response.\x1b[0m")
            print(goodbye_message)
            return
    else:
        print("\x1b[91mMythril verification failed.\x1b[0m")
        print(goodbye_message)
        return


def main():
    annotated_code, working_status, pairs, description, purpose = get_code_and_properties()
    completed_code = get_completed_code(
        annotated_code, working_status, description, purpose, pairs)
    completed_code = get_compilation_results(completed_code)
    instrumented_code, instrumented_file = get_instrumented_code(
        completed_code)
    mythril_sucess, mythril_results = get_verification_results(
        instrumented_code, instrumented_file)
    further_action(mythril_sucess, mythril_results, instrumented_code)


if __name__ == '__main__':
    main()
