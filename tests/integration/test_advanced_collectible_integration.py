import pytest
import time
from scripts.helper import LOCAL_BLOCKCHAIN_ENVIRONMENT, get_account, get_contract
from brownie import network
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible_integration():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip()
    advanced_collectible, create_tx = deploy_and_create()
    time.sleep(180)
    assert advanced_collectible.tokenCounter() == 1