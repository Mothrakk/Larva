import os
import subprocess

import LarvaLibs.Utility as Utility

class ProcessHandler:
    def __init__(self, script):
        self.script = script
        self.p = None

    def alive(self) -> bool:
        if self.p is None:
            return False
        return Utility.pid_alive(self.p.pid)

    def start(self, args: list) -> None:
        if self.alive():
            print(f"{self.script.name} is already running")
        else:
            script_status = self.script.good_status()
            if script_status[0]:
                self.p = subprocess.Popen(f"python.exe {self.script.path} {' '.join(args)}")
                print(f"Started {self.script.name}")
            else:
                print(script_status[1])

    def kill(self) -> None:
        if self.alive():
            self.p.kill()
            self.p = None
            print(f"Killed {self.script.name}")
        else:
            print(f"{self.script.name} is not running")
