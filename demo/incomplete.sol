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

  function transfer(address _to, uint256 _value) external returns (bool) {
  }

  function approve(address _spender, uint256 _value) external returns (bool) {
  }

  function transferFrom(address _from, address _to, uint256 _value) external returns (bool) {
  }

  event Transfer(address indexed _from, address indexed _to, uint256 _value);
  event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}