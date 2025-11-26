"""Password Hacker with Python - Hack Module"""
import socket
from argparse import ArgumentParser, Namespace


def parse_arguments() -> Namespace:
    """Parse command line arguments"""
    parser = ArgumentParser()
    parser.add_argument("ip", type=str, help="IP Address")
    parser.add_argument("port", type=int, help="Port")
    parser.add_argument("msg", type=str, help="Message to send")
    args = parser.parse_args()
    return args

def send_message(host: str, port: int, message: str) -> str:
    # TCP client
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(5)  # optional
        sock.connect((host, port))
        sock.sendall(message.encode("utf-8"))
        # Receive (may need loop for larger data)
        data = sock.recv(4096)
        return data.decode("utf-8", errors="replace")



def main():
    args = parse_arguments()
    response = send_message(args.ip, args.port, args.msg)
    print(response)

if __name__ == "__main__":
    main()
