import argparse
import asyncio
import toml
import os


def read_config():
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    config_path = os.path.join(parent_dir, 'config.toml')

    with open(config_path) as f:
        with open('config.toml') as f:
            config = toml.load(f)

        print(config['address'])
        print(config['username'])
        print(config['password'])

async def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('number_sender', type=str)
    parser.add_argument('number_receiver', type=str)
    parser.add_argument('message', type=str)


    args = parser.parse_args()


    print(args.number_sender)
    print(args.number_receiver)
    print(args.message)

    read_config()
if __name__ == "__main__":
    asyncio.run(main())