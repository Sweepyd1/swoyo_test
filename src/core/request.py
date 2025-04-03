from typing import Dict
class HTTPRequest:
    def __init__(self, method:str, path:str, headers:Dict[str, str], body:bytes):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body

    def to_bytes(self) -> bytes:
        headers = self.headers.copy()
        headers["Content-Length"] = str(len(self.body))
        headers_str = "\r\n".join([f"{k}: {v}" for k, v in headers.items()])
        request_line = f"{self.method} {self.path} HTTP/1.1\r\n"
        return f"{request_line}{headers_str}\r\n\r\n".encode() + self.body


