import pytest
from scripts.advanced_collectible.create_metadata import upload_to_ipfs
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import network

def test_can_upload_to_ipfs():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    filepath = "./img/pug.png"
    image_url = upload_to_ipfs(filepath)
    assert image_url is not None and image_url != ""
