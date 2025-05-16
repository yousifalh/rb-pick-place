from requests import post, put
import socket
import struct
import time
# import bs4

"""
Wrapper that manages controller of robot through RobotWebServices
"""


CONTROLLER_IP = "192.168.0.1" 
PORT = 1025
BASE_URL = f"http://{CONTROLLER_IP}/rw"
TIMEOUT_S = 5.0


HEADERS = {
    "Content-Type" : "application/json",
    "Accept" : "application/json"
    #  Check if RWS for our controller requires authentication
    # "Authorization" : "Bearer --access token--"
}

# particularly interested in following directories:
# - rw/mastership/[request | release]/[e]
# - rw/rapid


class RobotWebService:
    """
    A wrapper for communicating to robot controller through
    ABB RobotWebService.
    Functions for upload, deletion and execution of RAPID programs
    -   Control program upload without having to have a USB to transfer 
        to pendant.
    """
    
    # TODO: Close iteration to figure out what exact headers are needed
        # - Robot working required

    def __init__(self,
            base_url: str=BASE_URL,
            headers: dict[str, str]=HEADERS) -> None:
        self.__base_url: str = base_url
        self.__headers: dict[str, str] = headers
            
    def acquire_mastership(self) -> bool:
        url = f"{self.__base_url}/mastership/acquire"
        response = post(url, headers=self.__headers)

        if response.ok:
            print("Mastership of robot acquired!")
            return True
        else:
            print("ERROR: Failed to acquire mastership.")
            return False
        
    def upload_rapid_program(self, fp: str, prog_name: str) -> bool:
        # /fileservice/{device|environment_variable|directory}/{file}
        
        url = f"{self.__base_url}/fileservice/{prog_name}"
        with open(fp, 'rb') as file:
            response = put(url, headers=self.__headers, data=file)
    
    def execute_rapid_program(self, prog_fp: str) -> bool:
        pass

class ABBClient:
    def __init__(self, host=CONTROLLER_IP, port=PORT):
        self.host, self.port = host, port
        self.sock: socket.socket | None = None

    # ─────────────────────────────────────────────
    # Low-level connection handling
    # ─────────────────────────────────────────────
    def connect(self) -> None:
        """Open the TCP socket and run READY/ACK handshake."""
        self.sock = socket.create_connection((self.host, self.port), TIMEOUT_S)
        self.sock.settimeout(TIMEOUT_S)

        # 1) Tell the robot we are ready
        self._send(b"READY\n")

        # 2) Wait for ACK (blocks ≤ TIMEOUT_S)
        ack = self._recv_line()
        if ack != b"ACK":
            raise RuntimeError(f"Unexpected handshake reply: {ack!r}")
        print("[+] Connected & hand-shaken")

    def close(self) -> None:
        if self.sock:
            try:
                self.sock.close()
            finally:
                self.sock = None
        print("[–] Socket closed")

    # ─────────────────────────────────────────────
    # Public API
    # ─────────────────────────────────────────────
    def send_xy(self, x: float, y: float) -> None:
        """Send a single coordinate pair as ASCII 'x,y\\n'."""
        if self.sock is None:
            self.connect()
        msg = f"{x:.6f},{y:.6f}\n".encode("ascii")
        self._send(msg)

    # ─────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────
    def _send(self, data: bytes) -> None:
        totalsent = 0
        while totalsent < len(data):
            sent = self.sock.send(data[totalsent:])
            if sent == 0:
                raise ConnectionError("Socket connection broken")
            totalsent += sent

    def _recv_line(self) -> bytes:
        """Receive until '\\n'; returns line without terminator."""
        data = bytearray()
        while True:
            chunk = self.sock.recv(1)
            if not chunk:
                raise ConnectionError("Peer closed before newline")
            if chunk == b"\n":
                return bytes(data).rstrip(b"\r")
            data.extend(chunk)


