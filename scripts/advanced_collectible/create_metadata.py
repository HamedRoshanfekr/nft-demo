from brownie import AdvancedCollectible, network
from scripts.helper import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json
import os

def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectible = advanced_collectible.tokenCounter()
    print(f"you have {number_of_advanced_collectible} advanced collectible")
    for token_id in range(number_of_advanced_collectible):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        collectible_metadata = metadata_template
        metadata_file_name = f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} is already exists. delete to overwrite")
        else:
            print(f"creating metadata file {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pop!"
            image_path = f"./img/" + breed.lower().replace("_", "-") + ".png"
            image_uri = upload_to_ipfs(image_path)
            collectible_metadata["image"] = image_uri
            os.makedirs(os.path.dirname(metadata_file_name), exist_ok=True)
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(file_path):
    with Path(file_path).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files= {"file":image_binary})
        ipfs_hash = response.json()["Hash"]
        file_name = file_path.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={file_name}"
        print(image_uri)
        return image_uri