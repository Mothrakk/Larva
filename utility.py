import datetime
import time
import os
import sys

def TICKRATE() -> float:
    """Returns the global tickrate used in Larva and its subprocesses."""
    return 0.1

def tick() -> float:
    """Sleep for TICKRATE() seconds. Returns TICKRATE()."""
    time.sleep(TICKRATE())
    return TICKRATE()

def file_read(path: str) -> str:
    """Wrapper function to read from a file in one line.
    
    Returns empty string if file doesn't exist."""
    out = ""
    if os.path.isfile(path):
        with open(path, "r") as fptr:
            out = fptr.read()
    return out

def file_write(path: str, contents="", mode="w") -> None:
    """Wrapper function to write to a file in one line."""
    with open(path, mode) as fptr:
        fptr.write(f"{contents}\n")

def file_flush(path: str) -> str:
    """Read from a file and return the contents, leaving the file empty afterwards.
    
    Returns empty string is file doesn't exist."""
    contents = file_read(path)
    file_write(path)
    return contents

def timestamp() -> str:
    """Returns a timestamp in the form of %H:%M:%S"""
    return f"[{datetime.datetime.now().strftime('%H:%M:%S')}]"

def pid_alive(pid) -> bool:
    """Check if given process (pid) is still alive."""
    try:
        os.kill(int(pid), 0)
        return True
    except OSError:
        return False

def pipe_path(name: str, extension=".txt") -> str:
    """Build a path to the filename in the pipeline folder."""
    return f"pipeline\\{name}{extension}"
