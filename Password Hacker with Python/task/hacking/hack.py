"""Password Hacker with Python - Hack Module"""

from argparse import ArgumentParser, Namespace


def parse_arguments() -> Namespace:
    """Parse command line arguments"""
    parser = ArgumentParser()
    parser.add_argument("ip", type=str, help="IP Address")
    parser.add_argument("port", type=int, help="Port")
    parser.add_argument("msg", type=str, help="Message to send")
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()

if __name__ == "__main__":
    main()
