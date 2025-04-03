import pytest
from src.main import load_config
import os

@pytest.fixture
def temp_config(tmp_path):
    config_content = """
    [server]
    url = "http://test.com"
    
    [auth]
    username = "test_user"
    password = "test_pass"
    """
    config_file = tmp_path / "config.toml"
    config_file.write_text(config_content)
    return config_file

def test_load_config(temp_config) -> None:
    config = load_config(temp_config)
    assert config["server_url"] == "http://test.com"
    assert config["username"] == "test_user"
    assert config["password"] == "test_pass"