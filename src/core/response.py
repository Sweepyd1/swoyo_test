from typing import Self, Dict

class HTTPResponse:
    def __init__(self, status:int, headers:Dict[str, str], body:str):
        self.status = status
        self.headers = headers
        self.body = body

    @classmethod
    def from_bytes(cls, data:bytes) -> Self:
        try:
            headers_part, body = data.split(b"\r\n\r\n", 1)
        except ValueError:
            headers_part = data
            body = b""
        header_lines = headers_part.decode().split("\r\n")
        status_line = header_lines[0]
        status = int(status_line.split()[1])
        headers = {}
        for line in header_lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key] = value
        return cls(status, headers, body.decode())