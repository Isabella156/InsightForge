from openai import OpenAI
from solcx import compile_standard, install_solc, get_installed_solc_versions, set_solc_version
from solcx.exceptions import SolcError
import subprocess
import os

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

def run_scribble(code):
    original_filename = "original.sol"
    with open(original_filename, 'w') as file:
        file.write(code)
    print(f"Solidity code written to {original_filename}")
    flat_filename = original_filename.replace(".sol", ".flat.sol")
    try:
        command = [
            'scribble',
            original_filename,
            '--output-mode', 'flat',
            '--output', flat_filename,
            '--instrumentation-metadata-file', 'metadata'
        ]

        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print("Scribble instrumentation successful.")
        print(result.stdout)
        # instructed_wrong_filename = "original.sol.instrumented"
        # instructed_correct_filename = "original.instrumented.sol"
        # os.rename(instructed_wrong_filename, instructed_correct_filename)
        # TODO: reasonable return statement
        return result.stdout
    except subprocess.CalledProcessError as e:
        if not os.path.exists(flat_filename):
            print("Failed to run Scribble:")
            print(e.stderr)
            return None

def run_mythril(filename, parameters):
    command = [
            'myth',
            'analyze',
            filename,
            '-t', parameters["transaction_depth"],
            '--execution-timeout', parameters["execution_timeout"]
        ]
        # TODO: example for no security violations
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode == 0:
        print("Mythril verification successful.")
        print("Standard Output:", result.stdout)
    elif result.returncode == 1:
        print("Security violations:")
        print("Verification results:\n", result.stdout)  # Output may still be valuable
    else:
        print("An unexpected error occurred.")


