from main import annotate_code
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