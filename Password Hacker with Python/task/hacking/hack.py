"""Password Hacker with Python - Hack Module"""
import socket
from argparse import ArgumentParser, Namespace
import string
from itertools import product
from typing import Any, Generator


def parse_arguments() -> Namespace:
    """Parse command line arguments"""
    parser = ArgumentParser()
    parser.add_argument("ip", type=str, help="IP Address")
    parser.add_argument("port", type=int, help="Port")
    args = parser.parse_args()
    return args


def guess_password(max_length: int = 9) -> Generator[str, Any, None]:
    """Generate password guesses

    Try cartesian product of letters and digits up to max_length
    """

    alphabet = string.ascii_lowercase + string.digits
    for n in range(1, max_length + 1):
        for t in product(alphabet, repeat=n):
            yield ''.join(t)


def main():
    args = parse_arguments()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((args.ip, args.port))
    for guess in guess_password():
        client.send(guess.encode())
        response = client.recv(1024).decode()
        if response == "Connection success!":
            print(guess)
            client.close()
            return


if __name__ == "__main__":
    main()
