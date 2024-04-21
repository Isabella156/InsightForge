import json
import os
import subprocess

from openai import OpenAI
from solcx import compile_standard, get_installed_solc_versions, install_solc, set_solc_version
from solcx.exceptions import SolcError


def get_chatgpt_response(system_message, user_message):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    )
    return completion.choices[0].message.content


def compile_code(code):
    solc_version = '0.6.0'

    if solc_version not in get_installed_solc_versions():
        print(f"Installing solc version {solc_version}...")
        install_solc(solc_version)

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
        print("\x1b[94mCompiling code...\x1b[0m")
        compile_standard(compiled_input)
        print("\x1b[94mCompilation successful.\x1b[0m")
        return True
    except SolcError as e:
        print("\x1b[91mCompilation failed with errors:")
        print("x1b[91m", e, "\x1b[0m")
        return False


def run_scribble(code):
    original_filename = "original.sol"
    with open(original_filename, 'w') as file:
        file.write(code)
    print(f"Solidity code written to {original_filename}")
    flat_filename = "original.flat.sol"
    try:
        command = [
            'scribble',
            original_filename,
            '--output-mode', 'flat',
            '--output', flat_filename,
            '--instrumentation-metadata-file', 'metadata'
        ]

        subprocess.run(command, check=True,
                       text=True, capture_output=True)
        print("\x1b[94mScribble instrumentation successful.\x1b[0m")
        return flat_filename
    except subprocess.CalledProcessError as e:
        if not os.path.exists(flat_filename):
            print("\x1b[91mFailed to run Scribble:\x1b[0m")
            print("\x1b[91m", e.stderr, "\x1b[0m")
            return None


def run_mythril(filename, parameters):
    command = [
        'myth',
        'analyze',
        filename,
        '-t', parameters["transaction_depth"],
        '--execution-timeout', parameters["execution_timeout"],
        '--solver-timeout', parameters["solver_timeout"],
    ]
    # TODO: example for no security violations
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode == 0:
        print("\x1b[95mMythril verification successful.\x1b[0m")
        print("\x1b[95mStandard Output\n:", result.stdout, "\x1b[0m")
        return (True, result.stdout)
    elif result.returncode == 1:
        print("\x1b[91mSecurity violations:\x1b[0m")
        print("\x1b[91mVerification results:\n", result.stdout, "\x1b[0m")
        return (False, result.stdout)
    else:
        print("\x1b[91mAn unexpected error occurred.\x1b[0m")
        return (None, None)
