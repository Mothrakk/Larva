import datetime

def TICKRATE() -> float:
    """Returns the global tickrate used in Larva and its subprocesses."""
    return 0.1

def file_read(path: str) -> str:
    """Wrapper function to read from a file in one line."""
    with open(path, "r") as fptr:
        return fptr.read()

def file_write(path: str, contents="", mode="w") -> None:
    """Wrapper function to write to a file in one line."""
    with open(path, mode) as fptr:
        fptr.write(f"{contents}\n")

def file_flush(path: str):
    """Read from a file and return the contents, leaving the file empty afterwards."""
    contents = file_read(path)
    file_write(path)
    return contents

def pipe_path(name: str) -> str:
    """Build a path to the filename in the pipeline folder."""
    return f"pipeline\\{name}.txt"

def timestamp() -> str:
    """Returns a timestamp in the form of %H:%M:%S"""
    return f"[{datetime.datetime.now().strftime('%H:%M:%S')}]"

def build_log(contents: str, name: str, timestamp=True):
    """Construct a pretty log to pass into Larva."""
    return f"{timestamp() }" * timestamp + f"{name}: {contents}"

def write_to_larva(log: str):
    """Write the log to Larva."""
    file_write(pipe_path("larva"), log, "a")
