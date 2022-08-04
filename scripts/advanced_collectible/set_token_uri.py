from brownie import network, AdvancedCollectible
from scripts.helper import get_breed, get_account, OPENSEA_URL

dog_metadata_dic = {
    "PUG": "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "SHIBA_INU": "ipfs://QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "ipfs://QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}

def main():
    print(f"working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectible = advanced_collectible.tokenCounter()
    print(f"you have {number_of_advanced_collectible} advanced collectible")
    for token_id in range(number_of_advanced_collectible):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"setting token uri of {token_id}")
            set_token_uri(token_id, advanced_collectible, dog_metadata_dic[breed])


def set_token_uri(token_id, nft_contract, token_uri):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, token_uri, {"from": account})
    tx.wait(1)
    print(f"you can view your nft at {OPENSEA_URL.format(nft_contract.address, token_id)}")
    print("please wait up to 20 minutes and then click on refresh metadata button")