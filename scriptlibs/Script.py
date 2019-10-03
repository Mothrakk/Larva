import subprocess
import os
import utility

class Script:
    def __init__(self, path: str):
        self.path = path
        self.name, self.extension = path.split("\\")[-1].split(".")
        self.p = None
    
    def start(self) -> None:
        if self.p is not None:
            utility.write_to_larva(utility.build_log("Already started", self.name))
        else:
            self.p = subprocess.Popen(f"pythonw.exe {self.path} {os.getpid()}")
            utility.write_to_larva(utility.build_log("Started", self.name))

    def kill(self) -> None:
        if self.p is None:
            utility.write_to_larva(utility.build_log("Can't kill what isn't started", self.name))
        else:
            self.p.kill()
            self.p = None
            utility.write_to_larva(utility.build_log("Killed", self.name))
