from brownie import AdvancedCollectible, config, network
from scripts.helper import get_account, OPENSEA_URL, get_contract, fund_with_link


def deploy_and_create():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(get_contract("vrf_coordinator"),
                                                      get_contract("link_token"),
                                                      config["networks"][network.show_active()]["fee"],
                                                      config["networks"][network.show_active()]["keyhash"],
                                                      {"from": account})
    fund_with_link(advanced_collectible.address)
    create_tx = advanced_collectible.createCollectible({"from": account})
    create_tx.wait(1)
    print("new token has been created")
    return advanced_collectible , create_tx



def main():
    deploy_and_create()
