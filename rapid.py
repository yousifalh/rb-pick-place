import re


# provides tools for rapid programs
# upload, update, execution

# "combines simulation data"

def load_program(fp: str) -> str:
    prgm: str = ""
    with open(fp, 'r') as f:
        lines = f.readlines()
        for line in lines:
            prgm += line
    return prgm



