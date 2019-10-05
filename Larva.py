import subprocess
import os
import utility

class Log:
    def __init__(self, contents: str, name="", use_timestamp=True):
        self.contents = contents
        self.name = name
        self.use_timestamp = use_timestamp
    
    def build(self) -> str:
        log = f"{utility.timestamp()} " * self.use_timestamp
        if self.name:
            log += f"{self.name}: "
        log += self.contents
        return log

    def to_larva(self, method=False) -> None:
        """Display the log.

        `method: False` print() the log.

        `method: True` use the pipeline."""
        if method:
            utility.file_write(utility.pipe_path("larva"), self.build(), "a")
        else:
            print(self.build())

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
        contents = utility.file_read(self.cfg_path).strip().split("\n")
        keys_required = Script.REQUIRED_CFG_SETTINGS.keys()
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
        contents = utility.file_read(self.cfg_path).strip().split("\n")
        for line in contents:
            key, value = line.split(":")
            cfg[key] = value
        return cfg

    def good_status(self) -> tuple:
        """Return if script /should/ be good for launch.
        
        Return value is a tuple in the form of: (good_status: bool , err_log: Log)
        """
        if not os.path.isfile(self.path):
            return (False, Log(f"Missing file: {self.filename}", self.name))
        if not self.valid_cfg():
            return (False, Log("Corrupted cfg file", self.name))
        return (True, None)

    def proc_start(self) -> None:
        self.prochandler.start()

class ProcessHandler:
    def __init__(self, script: Script):
        self.script = script
        self.p = None

    def alive(self) -> bool:
        if self.p is None:
            return False
        return utility.pid_alive(self.p.pid)

    def start(self) -> None:
        if self.alive():
            Log(f"{self.script.name} is already running").to_larva()
        else:
            script_status = self.script.good_status()
            if script_status[0]:
                self.p = subprocess.Popen(f"pythonw.exe {self.script.path} {os.getpid()}")
                Log("Started", self.script.name).to_larva()
            else:
                script_status[1].to_larva()

class Larva:
    def __init__(self):
        os.makedirs("scripts")
        os.makedirs("pipeline")
        self.scripts = list()
        for x in os.listdir("scripts"):
            if len(x.split(".")) == 1:
                self.scripts.append(Script(f"scripts\\{x}"))
        for s in self.scripts:
            if s.valid_cfg() and s.cfg()["autostart"] == "1":
                s.proc_start()
