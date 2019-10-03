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
            l = utility.build_log("Already started", self.name)
            utility.write_to_larva(l)
        else:
            self.p = subprocess.Popen(f"start /B pythonw.exe {self.path} {os.getpid()}",
                                      shell=True)

    def kill(self) -> None:
        if self.p is None:
            l = utility.build_log("Can't kill what isn't started", self.name)
            utility.write_to_larva(l)
        else:
            self.p.kill()
            self.p = None

class ScriptManager:
    def __init__(self) -> None:
        self.scripts = []
        for x in os.listdir("scripts"):
            if len(x.split(".")) == 1:
                pass