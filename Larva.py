import subprocess
import os
import sys
import utility

class Log:
    def __init__(self, contents: str, use_timestamp=True):
        self.contents = str(contents)
        self.name = sys.argv[0].split("\\")[-1].split(".")[0]
        self.use_timestamp = use_timestamp

    def build(self) -> str:
        log = f"{utility.timestamp()} " * self.use_timestamp
        log += f"{self.name}: {self.contents}"
        return log

    def to_larva(self) -> None:
        """Display the log using the pipeline."""
        utility.file_write(utility.pipe_path("larva"), self.build(), "a")

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
        contents = utility.file_read(self.cfg_path).strip().split("\n")
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
            return (False, f"{self.name}: Missing file: {self.filename}")
        if not self.valid_cfg():
            return (False, f"{self.name}: Corrupted cfg file")
        return (True, None)

    def proc_start(self) -> None:
        """Ask the process handler to start the process."""
        self.prochandler.start()

    def kill(self) -> None:
        """Ask the process handler to kill the process."""
        self.prochandler.kill()

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
            print(f"{self.script.name} is already running")
        else:
            script_status = self.script.good_status()
            if script_status[0]:
                self.p = subprocess.Popen(f"pythonw.exe {self.script.path} {os.getpid()}")
                print(f"Started {self.script.name}")
            else:
                print(script_status[1])

    def kill(self) -> None:
        if self.p is not None:
            self.p.kill()
            self.p = None
            print(f"Killed {self.script.name}")
        else:
            print(f"{self.script.name} is not running")

class Larva:
    def __init__(self):
        self.HARDCOMMANDS = {
            "help":self.help,
            "exit":self.e,
            "cls":self.clear,
            "start":self.start,
            "kill":self.kill
        }
        self.create_missing_folders()
        self.scripts = self.build_scripts_dict()
        self.handle_autostart_scripts()

    def create_missing_folders(self) -> None:
        """Setup func - create folders."""
        for f in ("scripts", "pipeline"):
            if f not in os.listdir():
                os.makedirs(f)

    def build_scripts_dict(self) -> dict:
        """Setup func - populate dictionary."""
        scripts = dict()
        for name in os.listdir("scripts"):
            if len(name.split(".")) == 1:
                scripts[name] = Script(f"scripts\\{name}")
        return scripts

    def handle_autostart_scripts(self) -> None:
        """Attempt to start the scripts that are configured to be autostarted."""
        for s in self.scripts.values():
            if s.valid_cfg() and s.cfg()["autostart"] == "1":
                s.proc_start()

    def handle_scripts_input(self) -> None:
        contents = utility.file_flush(utility.pipe_path("larva"))
        if contents:
            print("\n".join(contents))

    def handle_kb_input(self, inp: str) -> None:
        inp = inp.strip().split(" ")
        if inp[0] in self.HARDCOMMANDS:
            self.HARDCOMMANDS[inp[0]](inp)
        elif inp[0] in self.scripts:
            utility.file_write(utility.pipe_path(inp[0]), ' '.join(inp[1:]), "a")

    def check_scripts_pulse(self) -> None:
        pass

    def help(self, inp: list) -> None:
        print(f"hcmds: {'; '.join(self.HARDCOMMANDS.keys())}")
        print(f"scripts: {'; '.join(self.scripts.keys())}")

    def e(self, inp: list) -> None:
        print("Exiting")
        exit(0)

    def clear(self, inp: list) -> None:
        subprocess.run("cls", shell=True)

    def start(self, inp: list) -> None:
        if len(inp) > 1:
            if inp[1] in self.scripts:
                self.scripts[inp[1]].proc_start()
            else:
                print(f"{inp[1]} not found")
        else:
            print("start {script name}")

    def kill(self, inp: list) -> None:
        if inp[1] in self.scripts:
            self.scripts[inp[1]].kill()
        else:
            print(f"{inp[1]} not found")
