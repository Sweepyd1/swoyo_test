import argparse
import base64
import json
import socket
from urllib.parse import urlparse
import tomli
import sys
from utils.request import HTTPRequest
from utils.response import HTTPResponse


def load_config(config_path):
    with open(config_path, "rb") as f:
        config = tomli.load(f)
    return {
        "server_url": config["server"]["url"],
        "username": config["auth"]["username"],
        "password": config["auth"]["password"],
    }

def parse_args():
    parser = argparse.ArgumentParser(description="Send SMS via CLI")
    parser.add_argument("--sender", required=True, help="Sender's phone number")
    parser.add_argument("--receiver", required=True, help="Recipient's phone number")
    parser.add_argument("--text", required=True, help="Message text")
    return parser.parse_args()

def main():
    args = parse_args()
    config = load_config("config.toml")
    
    body_data = {
        "sender": args.sender,
        "recipient": args.receiver,
        "message": args.text
    }
    body_json = json.dumps(body_data).encode("utf-8")
    
 
    credentials = f"{config['username']}:{config['password']}".encode()
    auth_header = base64.b64encode(credentials).decode()
    
    url = urlparse(config["server_url"])
    host = url.hostname
    port = url.port or 80
    path = url.path
    
    headers = {
        "Host": f"{host}:{port}" if port != 80 else host,
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth_header}"
    }
    

    request = HTTPRequest("POST", path, headers, body_json)
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(request.to_bytes())
            
            response_data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response_data += chunk
            
            response = HTTPResponse.from_bytes(response_data)
            print(f"Code: {response.status}")
            print(f"Body: {response.body}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()