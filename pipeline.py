import os
import sys

import pexpect


def test_terminal_output():
    child = pexpect.spawn('python main.py', timeout=60,
                          encoding='utf-8', logfile=sys.stdout)

    code = """pragma solidity ^0.6.0;

contract ERC20 {
  uint256 private _totalSupply;
  mapping (address => uint256) private _balances;
  mapping (address => mapping (address => uint256)) private _allowances;

  constructor() public {
    _totalSupply = 1000000;
    _balances[msg.sender] = 1000000;
  }

  function totalSupply() external view returns (uint256) {
    return _totalSupply;
  }

  function balanceOf(address _owner) external view returns (uint256) {
    return _balances[_owner];
  }

  function allowance(address _owner, address _spender) external view returns (uint256) {
    return _allowances[_owner][_spender];
  }

  function transfer(address _to, uint256 _value) external returns (bool) {
  }

  function approve(address _spender, uint256 _value) external returns (bool) {
  }

  function transferFrom(address _from, address _to, uint256 _value) external returns (bool) {
  }

  event Transfer(address indexed _from, address indexed _to, uint256 _value);
  event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}
"""
    child.sendline(code)
    child.sendline('exit')

    # Handle multiple expects to clear any residual escape sequences
    # child.expect(
    # r'Is your code complete or incomplete\? Enter \'Complete\' or \'Incomplete\':')
    child.sendline('Incomplete')  # Respond again if prompted again

    child.sendline('transfer')

    property = "#if_succeeds {:msg \"Transfer does not modify the sum of balances\"} old(_balances[_to]) + old(_balances[msg.sender]) == _balances[_to] + _balances[msg.sender];"
    child.sendline(property)
    function_description = "Transfers tokens from the message sender's account to another account."
    child.sendline(function_description)
    function_purpose = "To allow a token holder to transfer part of their balance to another account."
    child.sendline(function_purpose)
    function_preconditions = "The sender must have a balance greater than or equal to the value to be transferred."
    child.sendline(function_preconditions)
    child.sendline('')
    function_postconditions = "Decreases the sender's balance by the transferred value and increases the receiver's balance by the same amount. Emits a Transfer event."
    child.sendline(function_postconditions)
    child.sendline('')
    child.sendline('')

    code_description = "This Solidity file defines an ERC20 standard token contract. The ERC20 standard allows for the implementation of a standard API for tokens within smart contracts."
    child.sendline(code_description)
    child.sendline('exit')
    code_purpose = "The purpose of this contract is to create a fungible token system on the Ethereum blockchain. The tokens can be transferred between accounts and used in decentralized applications as a means of transaction or interaction."
    child.sendline(code_purpose)
    child.sendline('exit')

    completed_code = """
pragma solidity ^0.6.0;

contract ERC20 {
  uint256 private _totalSupply;
  mapping (address => uint256) private _balances;
  mapping (address => mapping (address => uint256)) private _allowances;

  constructor() public {
    _totalSupply = 1000000;
    _balances[msg.sender] = 1000000;
  }

  function totalSupply() external view returns (uint256) {
    return _totalSupply;
  }

  function balanceOf(address _owner) external view returns (uint256) {
    return _balances[_owner];
  }

  function allowance(address _owner, address _spender) external view returns (uint256) {
    return _allowances[_owner][_spender];
  }

  /// #if_succeeds {:msg "Transfer does not modify the sum of balances"} old(_balances[_to]) + old(_balances[msg.sender]) == _balances[_to] + _balances[msg.sender];
  function transfer(address _to, uint256 _value) external returns (bool) {
    address from = msg.sender;
    require(_value <= _balances[from]);


    uint256 newBalanceFrom = _balances[from] - _value;
    uint256 newBalanceTo = _balances[_to] + _value;
    _balances[from] = newBalanceFrom;
    _balances[_to] = newBalanceTo;

    emit Transfer(msg.sender, _to, _value);
    return true;
  }

  function approve(address _spender, uint256 _value) external returns (bool) {
    address owner = msg.sender;
    _allowances[owner][_spender] = _value;
    emit Approval(owner, _spender, _value);
    return true;
  }

  function transferFrom(address _from, address _to, uint256 _value) external returns (bool) {
    uint256 allowed = _allowances[_from][msg.sender];
    require(_value <= allowed);
    require(_value <= _balances[_from]);
    _balances[_from] -= _value;
    _balances[_to] += _value;
    _allowances[_from][msg.sender] -= _value;
    emit Transfer(_from, _to, _value);
    return true;
  }

  event Transfer(address indexed _from, address indexed _to, uint256 _value);
  event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}
"""
    child.sendline(completed_code)
    child.sendline('exit')

    child.sendline('')
    child.sendline('')
    child.sendline('')

    child.sendline('Exit the program')

    # Wait until the end of the session
    child.expect(pexpect.EOF)
    output = child.before

    # Print output or perform checks
    print("final output")
    print(output)


if __name__ == '__main__':
    # os.environ['TERM'] = 'vt100'
    os.environ['TERM'] = 'dumb'
    test_terminal_output()
