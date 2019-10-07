import os
import datetime
import subprocess
import time
import sys

def TICKRATE() -> float:
    """Returns the global tickrate used in Larva's subprocesses."""
    return 0.3

def tick() -> float:
    """Sleep for TICKRATE() seconds. Returns TICKRATE()."""
    time.sleep(TICKRATE())
    return TICKRATE()

def file_read(path: str) -> str:
    """Wrapper function to read from a file in one line.
    
    Returns empty string if file doesn't exist."""
    if os.path.isfile(path):
        with open(path, "r") as fptr:
            return fptr.read()
    return ""

def file_write(path: str, contents="", mode="w") -> None:
    """Wrapper function to write to a file in one line."""
    with open(path, mode) as fptr:
        fptr.write(f"{contents}\n")

def file_flush(path: str) -> list:
    """Read from a file and return the contents as a list split by newlines, leaving the file empty afterwards.
    
    Returns empty list is file doesn't exist."""
    contents = file_read(path).strip()
    if not contents:
        return []
    file_write(path)
    return [line for line in contents.split("\n") if line]

def timestamp() -> str:
    """Returns a timestamp in the form of %H:%M:%S"""
    return f"[{datetime.datetime.now().strftime('%H:%M:%S')}]"

def pid_alive(pid) -> bool:
    """Check if given process (pid) is still alive."""
    capture = subprocess.run(f'TASKLIST /FO CSV /FI "PID eq {pid}"', capture_output=True)
    capture = str(capture.stdout).split(r"\n")[1].split(",")
    return capture != ["'"] and capture[0] == '"python.exe"'

def pipe_path(name: str, extension=".txt") -> str:
    """Build a path to the filename in the pipeline folder."""
    return f"pipeline\\{name}{extension}"