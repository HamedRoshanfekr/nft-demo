import pytest

from scripts.helper import LOCAL_BLOCKCHAIN_ENVIRONMENT, get_account, get_contract
from brownie import network
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip()
    advanced_collectible, create_tx = deploy_and_create()
    request_id = create_tx.events["requestedCollectible"]["requestId"]
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(request_id, random_number, advanced_collectible.address,
                                                           {"from": get_account()})
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3