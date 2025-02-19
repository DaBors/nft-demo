import json
import os
from pathlib import Path
from brownie import AdvancedCollectible, network
from metadata.sample_metadata import metadata_template
import requests

from scripts.helpful_scripts import get_breed

breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}

breed_to_animation_uri = {
    "PUG": "https://ipfs.io/ipfs/QmQKJGYaRunwnBWHLyG2ZC2tSkaFRbdo7wMxidGwrxoS5u?filename=pug.html",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmZMhTDssSf7Et7Z3BLii8m8TUZe1uXidVuBpVsUGMLJHR?filename=shiba-inu.html",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmesstDKshuTFZJjTaiNkMtLrCGiVgsTa97AuW8aWdoS1T?filename=st-bernard.html",
}


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup!"
            
            image_path = f"./img/{breed.lower().replace('_','-')}.png"
            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]
            collectible_metadata["image"] = image_uri
            
            animation_path = f"./img/{breed.lower().replace('_','-')}.html"
            animation_url = None
            if os.getenv("UPLOAD_IPFS") == "true":
                animation_url = upload_to_ipfs(animation_path)
            animation_url = animation_url if animation_url else breed_to_animation_uri[breed]
            collectible_metadata["animation_url"] = animation_url
            
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
