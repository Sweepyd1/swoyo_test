import pytest
from src.main import main
from unittest.mock import patch, MagicMock, call

@pytest.fixture
def mock_socket():
    with patch("socket.socket") as mock_socket:
  
        mock_instance = MagicMock()
        mock_instance.recv.side_effect = [
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: application/json\r\n"
            b"Content-Length: 21\r\n"
            b"\r\n"
            b'{"status": "success"}',
            b''  
        ]
        mock_socket.return_value.__enter__.return_value = mock_instance
        yield mock_instance

def test_main_success(mock_socket, capsys):
    with patch("src.main.load_config") as mock_load:
        mock_load.return_value = {
            "server_url": "http://test.com/api/send",
            "username": "user",
            "password": "pass"
        }
        
        with patch("sys.argv", [
            "main.py",
            "--sender", "123",
            "--receiver", "456",
            "--text", "Test"
        ]):
            main()
            
   
    captured = capsys.readouterr()
    assert "Code: 200" in captured.out
    assert "Body: {\"status\": \"success\"}" in captured.out

    sent_data = mock_socket.sendall.call_args[0][0]
    request_body = sent_data.decode().split("\r\n\r\n")[1]
    print("\nТело запроса:", request_body)  
    
    assert b"POST /api/send HTTP/1.1" in sent_data
    assert b'"sender": "123"' in sent_data
    assert b'"recipient": "456"' in sent_data  
    assert b'"message": "Test"' in sent_data