import pytest

from scripts.helper import LOCAL_BLOCKCHAIN_ENVIRONMENT, get_account
from brownie import network
from scripts.simple_collectible.deploy_and_create import deploy_and_create

def test_can_create_simple_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip()
    simple_collectible = deploy_and_create()
    assert simple_collectible.ownerOf(0) == get_account()
