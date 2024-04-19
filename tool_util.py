from openai import OpenAI

from solcx import compile_standard, install_solc, get_installed_solc_versions, set_solc_version

from solcx.exceptions import SolcError

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