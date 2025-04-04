import pytest
from src.core.request import HTTPRequest
from src.core.response import HTTPResponse

class TestHTTPRequest:
    def test_to_bytes(self) -> None:
        request = HTTPRequest(
            method="POST",
            path="/send_sms",
            headers={"Content-Type": "application/json"},
            body=b'{"test": true}'
        )
        result = request.to_bytes()
        assert b"POST /send_sms HTTP/1.1" in result
        assert b"Content-Type: application/json" in result
        assert b'{"test": true}' in result

class TestHTTPResponse:
    @pytest.fixture
    def sample_response(self):
        data = (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: application/json\r\n"
            b"\r\n"
            b'{"status": "success"}'
        )
        return HTTPResponse.from_bytes(data)
 
    def test_from_bytes(self, sample_response) -> None:
        assert sample_response.status == 200
        assert sample_response.headers["Content-Type"] == "application/json"
        assert sample_response.body == '{"status": "success"}'