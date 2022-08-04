from brownie import accounts, network, config, VRFCoordinatorMock, LinkToken, interface, Contract


FORKED_LOCAL_ENVIRONMENT = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENT = ["development", "ganache-local"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

DECIMALS = 8
STARTING_PRICE = 200000000000

contract_to_mock = {"vrf_coordinator": VRFCoordinatorMock,
                    "link_token": LinkToken}

BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}

def get_breed(breed_number):
    return BREED_MAPPING[breed_number]


def get_account(index=None, _id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT or network.show_active() in FORKED_LOCAL_ENVIRONMENT:
        return accounts[0]
    if _id:
        return accounts.load(_id)
    return accounts.add(config["wallets"]["from_key"])

def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
        print(f"contract address of {contract_name} is {contract_address}")
    return contract


def deploy_mocks(decimals=DECIMALS, starting_price=STARTING_PRICE):
    account = get_account()
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})

def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    # tx = link_token.transfer(contract_address, amount, {"from": account})
    link_token_contract = interface.LinkTokenInterface(link_token.address)
    tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("funded link")
    return tx

def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    # tx = link_token.transfer(contract_address, amount, {"from": account})
    link_token_contract = interface.LinkTokenInterface(link_token.address)
    tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("funded link")
    return tx