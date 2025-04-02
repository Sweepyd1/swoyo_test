from src.main import parse_args
import pytest
from unittest.mock import patch

def test_parse_args():
    test_args = [
        "--sender", "123",
        "--receiver", "456",
        "--text", "Test message"
    ]
    with patch("sys.argv", ["main.py"] + test_args):
        args = parse_args()
        assert args.sender == "123"
        assert args.receiver == "456"
        assert args.text == "Test message"