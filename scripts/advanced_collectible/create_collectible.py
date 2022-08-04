from brownie import AdvancedCollectible
from scripts.helper import get_account, fund_with_link

def main():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(advanced_collectible.address)
    create_tx = advanced_collectible.createCollectible({"from": account})
    create_tx.wait(1)
    print("collectible created")