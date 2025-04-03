import argparse
import base64
import json
import socket
from urllib.parse import urlparse
import tomli
import sys
from core.request import HTTPRequest
from core.response import HTTPResponse
import asyncio
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('sms_client.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)



def load_config(config_path: str, logger:logging.Logger) -> dict:
    try:
        with open(config_path, "rb") as f:
            config = tomli.load(f)
        logger.info(f"Config loaded from {config_path}")
        return {
            "server_url": config["server"]["url"],
            "username": config["auth"]["username"],
            "password": config["auth"]["password"],
        }
    except Exception as e:
        logger.error(f"Error loading config: {str(e)}")
        raise

def parse_args(logger: logging.Logger) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send SMS via CLI")
    parser.add_argument("--sender", required=True, help="Sender's phone number")
    parser.add_argument("--receiver", required=True, help="Recipient's phone number")
    parser.add_argument("--text", required=True, help="Message text")
    args = parser.parse_args()
    
    logger.info(f"CLI arguments parsed: sender={args.sender}, "
                f"receiver={args.receiver}, text_length={len(args.text)}")
    return args

async def main() -> None:
    logger = setup_logging()
    logger.info("Starting SMS client")
    args = parse_args(logger)
    config = load_config("config.toml", logger)
    
    body_data = {
        "sender": args.sender,
        "recipient": args.receiver,
        "message": args.text
    }
    logger.debug(f"Request body: {body_data}")
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
    logger.info(f"Sending request to {config['server_url']}")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(await request.to_bytes())
            
            response_data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response_data += chunk
            
            response = await HTTPResponse.from_bytes(response_data)
            logger.info(f"Received response: {response.status}")
            logger.debug(f"Response body: {response.body}")

            print(f"Code: {response.status}")
            print(f"Body: {response.body}")
    
    except Exception as e:
        logger.error(f"Critical error: {str(e)}", exc_info=True)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())