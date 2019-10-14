import os

import LarvaLibs.Utility as Utility
from LarvaLibs.Script import Script
from LarvaLibs.Hardcodes import Hardcodes

class Larva:
    def __init__(self):
        self.hardcodes = Hardcodes(self)
        self.hardcodes.clear(None)
        self.create_missing_folders()
        self.scripts = self.build_scripts_dict()
        self.handle_autostart_scripts()
        self.hardcodes.help(None)

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
        contents = Utility.file_flush(Utility.pipe_path("larva"))
        if contents:
            print("\n".join(contents))

    def handle_kb_input(self, inp: str) -> None:
        inp = inp.strip().split(" ")
        if inp[0] in self.hardcodes.d:
            self.hardcodes.d[inp[0]](inp)
        elif inp[0] in self.scripts:
            Utility.file_write(Utility.pipe_path(inp[0]), ' '.join(inp[1:]), "a")
        else:
            print(f"Unknown command: {inp[0]}, try running 'help'")

    def check_scripts_pulse(self) -> None:
        pass
