from main import annotate_code

function_properties = {
    "totalSupply": {
        "property": "",
        "description": "Retrieves the total supply of tokens.",
        "purpose": "Allows users to check the total number of tokens available in the system.",
        "preconditions": ["None (since it only returns a state variable)."],
        "postconditions": ["Returns the current state of the _totalSupply variable."]
    },
    "balanceOf": {
        "property": "",
        "description": "Provides the balance of tokens held by a specific account.",
        "purpose": "Enables account holders or others to verify the amount of tokens an account holds.",
        "preconditions": ["None (as it only accesses and returns a state variable)."],
        "postconditions": ["Returns the balance of the specified account."]
    },
    "allowance": {
        "property": "",
        "description": "Returns the amount of tokens that an owner allowed a spender to use.",
        "purpose": "Allows checking the maximum amount of tokens that can be transferred from an owner’s account by a spender.",
        "preconditions": ["None (it simply returns a value from a mapping)."],
        "postconditions": ["Outputs the amount of tokens spender is allowed to transfer on behalf of owner."]
    },
    "transfer": {
        "property": "#if_succeeds {:msg \"Transfer does not modify the sum of balances\"} old(_balances[_to]) + old(_balances[msg.sender]) == _balances[_to] + _balances[msg.sender];",
        "description": "Transfers tokens from the message sender's account to another account.",
        "purpose": "To allow a token holder to transfer part of their balance to another account.",
        "preconditions": ["The sender must have a balance greater than or equal to the value to be transferred."],
        "postconditions": ["Decreases the sender's balance by the transferred value and increases the receiver's balance by the same amount.", "Emits a Transfer event."]
    },
    "approve": {
        "property": "",
        "description": "Allows a token holder to approve another account to spend a specified amount of tokens on their behalf.",
        "purpose": "To enable delegated spending of tokens up to a specified limit.",
        "preconditions": ["The owner (caller of the function) is in control of the tokens they are setting the allowance for."],
        "postconditions": ["Sets the allowance mapping to allow the spender to use the specified amount of tokens on behalf of the owner.", "Emits an Approval event."]
    },
    "transferFrom": {
        "property": "",
        "description": "Facilitates the transfer of tokens from one account to another, using the allowance mechanism.",
        "purpose": "Enables a spender to transfer up to an allowed amount of tokens from the token owner's account to a third party.",
        "preconditions": [
            "The spender must have an allowance from the owner that is equal to or greater than the amount to be transferred.",
            "The owner must have a balance equal to or greater than the amount to be transferred."
        ],
        "postconditions": [
            "Decreases the owner's balance and the spender’s allowance by the amount of tokens transferred.",
            "Increases the recipient's balance by the transferred amount.",
            "Emits a Transfer event."
        ]
    }
}

def test():
    """easy test"""
    with open("code.sol", 'r') as file:
        code = file.read()
    working_status = True
    pairs = {'transfer': '#if_succeeds {:msg "Transfer does not modify the sum of balances"} old(_balances[_to]) + old(_balances[msg.sender]) == _balances[_to] + _balances[msg.sender];'}
    annotated_code = annotate_code(code, pairs)
    print("annotated code\n")
    print(annotated_code)
    description = "Defines an ERC20 token contract managing ownership and transfer\
        of fungible tokens."
    purpose = "Enables creation and management of a digital token system on Ethereum for\
        transfers and approvals."
    precondition = "The deployer initializes the contract with a specific total supply.\
        Users must have sufficient token balance for transfer-related operations."
    postcondition = "The total supply of tokens is fixed post-deployment. All token operations\
        are recorded and emit corresponding events for auditability and traceability."