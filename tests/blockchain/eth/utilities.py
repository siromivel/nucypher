from typing import List

from web3 import Web3

from nkms.blockchain.eth.agents import MinerAgent
from nkms.blockchain.eth.constants import NuCypherMinerConfig
from nkms.blockchain.eth.deployers import MinerEscrowDeployer


class MockNuCypherMinerConfig(NuCypherMinerConfig):
    """Speed things up a bit"""
    _hours_per_period = 1     # Hours
    _min_release_periods = 1  # Minimum switchlock periods


class MockMinerEscrowDeployer(MinerEscrowDeployer, MockNuCypherMinerConfig):
    """Helper class for MockMinerAgent, using a mock miner config"""


class MockMinerAgent(MinerAgent):
    """MinerAgent with faked config subclass"""
    _deployer = MockMinerEscrowDeployer


def generate_accounts(w3: Web3, quantity: int, wei_balance: int=None) -> List[str]:
    """
    Generate 9 additional unlocked accounts transferring wei_balance to each account on creation.
    """
    if wei_balance is None:
        one_million_ether = 10**6 * 10**18   # wei -> ether
        balance = one_million_ether

    tx_hashes = list()
    insecure_passphrase = 'this-is-not-a-secure-password'
    for _ in range(quantity):
        address = w3.personal.newAccount(insecure_passphrase)
        w3.personal.unlockAccount(address, passphrase=insecure_passphrase)

        tx = {'to': address, 'from': w3.eth.coinbase, 'value': balance}
        txhash = w3.eth.sendTransaction(tx)
        tx_hashes.append(txhash)

    accounts = len(w3.eth.accounts)
    fail_message = "There are more total accounts then the specified quantity; There are {} existing accounts.".format(accounts)
    assert accounts == 10, fail_message
    return tx_hashes
