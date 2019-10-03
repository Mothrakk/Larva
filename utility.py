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

def pipe_path(name: str, extension=".txt") -> str:
    """Build a path to the filename in the pipeline folder."""
    return f"pipeline\\{name}{extension}"

def timestamp() -> str:
    """Returns a timestamp in the form of %H:%M:%S"""
    return f"[{datetime.datetime.now().strftime('%H:%M:%S')}]"

def build_log(contents: str, name="", _timestamp=True):
    """Construct a pretty log to pass into Larva."""
    out = f"{timestamp()} " * _timestamp
    if name:
        out += f"{name}: "
    out += contents
    return out

def write_to_larva(log: str):
    """Write the log to Larva."""
    file_write(pipe_path("larva"), log, "a")

def my_name() -> str:
    """Get a process' own filename using argv."""
    return sys.argv[0].split("\\")[-1].split(".")[0]
