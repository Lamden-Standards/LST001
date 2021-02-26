# required, holds all account balances and allowances
balances = Hash(default_value=0)

# required for minting an initial supply
@construct
def seed(vk: str):
    balances[vk] = 1_000_000 # change this value to alter the inital token supply

# The main transfer function
@export
def transfer(amount: float, to: str):
    assert amount > 0, 'Cannot send negative balances!'

    assert balances[ctx.caller] >= amount, 'Not enough coins to send!'

    # remove amount from senders account
    balances[ctx.caller] -= amount
    # add amount to receivers account
    balances[to] += amount

# Call to get the current balance of an account
# Currenty in review to see if we need this in a "basic" token
@export
def balance_of(account: str):
    return balances[account]

# Call to get the current amount an account can spend on behalf of another
# Currenty in review to see if we need this in a "basic" token
@export
def allowance(owner: str, spender: str):
    return balances[owner, spender]

# Call to allow another account the abilty to transfer an amount on your behalf
@export
def approve(amount: float, to: str):
    assert amount > 0, 'Cannot send negative balances!'

    # Add the amount to the callers
    balances[ctx.caller, to] += amount
    return balances[ctx.caller, to]

# Call to spend an amount from another users account; requires prior approval by that account to you
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