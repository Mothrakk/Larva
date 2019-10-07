import os

import LarvaLibs.Utility as Utility
from LarvaLibs.ProcessHandler import ProcessHandler

class Script:
    REQUIRED_CFG_SETTINGS = {
        "autostart":("0", "1"),
        "infinite" :("0", "1")
    }

    def __init__(self, dir_path: str):
        self.dir_path = dir_path
        self.name = dir_path.split("\\")[-1]
        self.filename = f"{self.name}.py"
        self.path = f"{dir_path}\\{self.filename}"
        self.cfg_path = f"{dir_path}\\cfg.txt"
        self.prochandler = ProcessHandler(self)

    def valid_cfg(self) -> bool:
        """Check if the contents of the script's cfg file are valid."""
        if not os.path.isfile(self.cfg_path):
            return False
        contents = Utility.file_read(self.cfg_path).strip().split("\n")
        keys_required = set(Script.REQUIRED_CFG_SETTINGS.keys())
        for line in contents:
            line = line.split(":")
            if len(line) != 2:
                return False
            key, value = line
            if key in keys_required and value in Script.REQUIRED_CFG_SETTINGS[key]:
                keys_required.remove(key)
            else:
                return False
        return not len(keys_required)

    def cfg(self) -> dict:
        """Return the cfg in the form of a dictionary. Meant to be called after valid_cfg()."""
        cfg = dict()
        contents = Utility.file_read(self.cfg_path).strip().split("\n")
        for line in contents:
            key, value = line.split(":")
            cfg[key] = value
        return cfg

    def good_status(self) -> tuple:
        """Return if script /should/ be good for launch.
        
        Return value is a tuple in the form of: (good_status: bool , err_log: Log)
        """
        if not os.path.isfile(self.path):
            return (False, f"{self.name}: Missing file: {self.filename}")
        if not self.valid_cfg():
            return (False, f"{self.name}: Corrupted cfg file")
        return (True, None)

    def proc_start(self, args: list) -> None:
        """Ask the process handler to start the process.
        
        Inserts Larva's PID as the first argument."""
        self.prochandler.start([str(os.getpid())] + args)

    def kill(self) -> None:
        """Ask the process handler to kill the process."""
        self.prochandler.kill()
