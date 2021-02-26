# LST001 - Basic Token Interface v0.1 (under-revision)

## Goal
This standard will describe the variables and methods needed to create a basic token on the Lamden Blockchain.  Adherence to this standard ensures highest possible compatibility for your token.

## Changes
Discussion on finalizing this standard is taking place in the [Github Discussions](https://github.com/Lamden-Standards/LST001/discussions/2); With a current deadline of March 2nd, 2021. Anyone is welcome to join and comment. 

## Imports
- `none`

## Variables

### **balances**
This variable holds the main account balances for the contract  `balances[account]`.
It also uses a multi-hash to store allowances `balances[owner, spender]`.

- Type: `Hash`
    - default value: `0`
- Required: `True`

``` python
balances = Hash(default_value=0)
```

## Methods

### **seed**
This is the constructor method for smart contract. We will use it to mint an initial token supply.

- Decorator: @construct
- Public: `False` 
- arguments:
    - `vk`
        - type: `string`
        - description: The account provided will be minted the initial supply of tokens.
- state changes: `1`
- assertions: `none`
- return: `void`

``` python
@construct
def seed(vk: str):
    balances[vk] = 1_000_000
```

### **transfer**
This is the main transfer method for the token. 
This should only be called if the `caller` is sending their tokens directly.
To send tokens on behalf of another account use the `transfer_from` method.

- Decorator: `@export`
- Public: `True` 
- arguments:
    - `amount`
        - type: `float`
        - The amount of tokens to be transferred
    - `to`
        - type: `string`
        - The account to send the tokens to.
- state changes: `2`
- assertions:
    - `amount` must be greater-than 0
        - error: `Cannot send negative balances!`
    - `callers` token balance must be greater-than or equal to `amount`
        - error: `Not enough coins to send!`
- return: `void`

``` python
@export
def transfer(amount: float, to: str):
    assert amount > 0, 'Cannot send negative balances!'
    assert balances[ctx.caller] >= amount, 'Not enough coins to send!'

    # remove amount from senders account
    balances[ctx.caller] -= amount
    # add amount to receivers account
    balances[to] += amount
```

### **balance_of**
**[Currently in review (REV_01)](https://github.com/Lamden-Standards/LST001/discussions/2)**

This function will return the current balance of an account.

- Decorator: `@export`
- Public: `True` 
- arguments:
    - `account`
        - type: `string`
        - The account to lookup the balance for
- state changes: `1`
- assertions: `none`
- return: `float`

``` python
@export
def balance_of(account: str):
    return balances[account]
```

### **allowance**
**[Currently in review (REV_02)](https://github.com/Lamden-Standards/LST001/discussions/2)**

This method will return the amount that has been approved for one account to spend on behalf of another.

- Decorator: `@export`
- Public: `True` 
- arguments:
    - `owner`
        - type: `string`
        - The account account owner
    - `spender`
        - type: `string`
        - The account to lookup the allowance for
- state changes: `1`
- assertions: `none`
- return: `float`

``` python
@export
def allowance(owner: str, spender: str):
    return balances[owner, spender]
```


### **approve**
**[Currently in review (REV_03)](https://github.com/Lamden-Standards/LST001/discussions/2)**

This method will return add to the approval balance of the caller's account for the `to` address provided.

- Decorator: `@export`
- Public: `True` 
- arguments:
    - `amount`
        - type: `float`
        - The amount of approval to add to the `to` account
    - `to`
        - type: `string`
        - The account that will receive the approval amount
- state changes: `2`
- assertions: 
    - `amount` must be greater-than 0
        - error: `Cannot send negative balances!`
- return: `float`

``` python
@export
def approve(amount: float, to: str):
    assert amount > 0, 'Cannot send negative balances!'

    # Add the amount to the callers
    balances[ctx.caller, to] += amount
    return balances[ctx.caller, to]
```

### **transfer_from**
This method will allow a caller to spend tokens from another account. 
For this to work a prior call to `approve` is needed by the `main_account`  to set an `allowance` for the caller. 
Failure to set an allowance beforehand will cause the method to error.

- Decorator: `@export`
- Public: `True` 
- arguments:
    - `amount`
        - type: `float`
        - The amount of tokens to transfer from `main_account`
    - `to`
        - type: `string`
        - The account that the tokens will be sent to
    - `main_account`
        - type: `string`
        - The account the tokens will taken from
- state changes: `3`
- assertions: 
    - `amount` must be greater-than 0
        - error: `Cannot send negative balances!`
    - `caller` has an approval greater-than or equal to the transfer `amount`
        - error: `Not enough coins approved to send! You have X and are trying to spend X`
    - the token balance of `main_account` is greater-than or equal to the transfer `amount`
        - error: `Not enough coins to send!`
- return: `void`

``` python
@export
def transfer_from(amount: float, to: str, main_account: str):
    assert amount > 0, 'Cannot send negative balances!'

    assert balances[main_account, ctx.caller] >= amount, 'Not enough coins approved to send! You have {} and are trying to spend {}'\
        .format(balances[main_account, ctx.caller], amount)
    assert balances[main_account] >= amount, 'Not enough coins to send!'

    # reduce the approval amount by the amount being spent
    balances[main_account, ctx.caller] -= amount

    # remove amount spent from the main account
    balances[main_account] -= amount
    # add the amount spent to the receivers account
    balances[to] += amount
```
