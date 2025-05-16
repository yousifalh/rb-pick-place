from network import *
from detector import *
import socket

import numpy as np


CONTROLLER_IP = "192.168.0.1" 
PORT = 1025 # match port with one in rapid code
prog_name = "prog-a.rapid" # Most functional program

def rapid_setup():
    """Handles full upload and execution of program"""
    rb = RobotWebService()

    # Upload and execution of program from device
    o = rb.upload_rapid_program(
        "rapid_programs/prog-abstract.rapid",
        prog_name)
    
    if not o:
        print("RWS ERROR: Failed to upload")
        exit(-1)

    o = rb.execute_rapid_program(
        prog_name
    )

# Homography matrix
# TODO: Routine that calculates matrix from position 
# coord of camera relative to an known artifact (i.e corner of table)
H = np.array()

def identify_coords(capture):
    """
    H - A constant that depends on position and orientation of your camera.
    """
    pxl_coords: list = calculate_centroid(capture)
    return [H * pcoord for pcoord in pxl_coords]


if __name__ == '__main__':
    rapid_setup()
    
    # Vision 
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print('Camera: Failed to identify camera')
        

    rb = ABBClient(CONTROLLER_IP, PORT)
    try:
        rb.connect()
        coords = identify_coords(cap)

        # TODO: New structure for code required to enable 
        # a more dynamic update - however it would be reasonable to
        # wait for robot to work before adding this complexity
        for c in coords:
            rb.send_xy(c)

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")

    finally:
        rb.close()

    
    




    

    
