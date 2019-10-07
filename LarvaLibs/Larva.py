import os
import subprocess
import time

import LarvaLibs.Utility as Utility
from LarvaLibs.Script import Script

class Larva:
    def __init__(self):
        self.HARDCOMMANDS = {
            "help" :self.help,
            "exit" :self.e,
            "cls"  :self.clear,
            "start":self.start,
            "kill" :self.kill
        }
        self.create_missing_folders()
        self.scripts = self.build_scripts_dict()
        self.handle_autostart_scripts()

    def tick(self) -> float:
        """Sleep for x seconds. Return x."""
        time.sleep(0.1)
        return 0.1

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
        if inp[0] in self.HARDCOMMANDS:
            self.HARDCOMMANDS[inp[0]](inp)
        elif inp[0] in self.scripts:
            Utility.file_write(Utility.pipe_path(inp[0]), ' '.join(inp[1:]), "a")

    def check_scripts_pulse(self) -> None:
        pass

    def help(self, inp: list) -> None:
        print(f"cmds: {'; '.join(self.HARDCOMMANDS.keys())}")
        print(f"scripts: {'; '.join(self.scripts.keys())}")

    def e(self, inp: list) -> None:
        print("Exiting")
        exit(0)

    def clear(self, inp: list) -> None:
        subprocess.run("cls", shell=True)

    def start(self, inp: list) -> None:
        if len(inp) > 1:
            if inp[1] in self.scripts:
                self.scripts[inp[1]].proc_start(inp[2:])
            else:
                print(f"{inp[1]} not found")
        else:
            print("start {script name} {arg} {arg} ...")

    def kill(self, inp: list) -> None:
        if len(inp) > 1:
            if inp[1] in self.scripts:
                self.scripts[inp[1]].kill()
            else:
                print(f"{inp[1]} not found")
        else:
            print("kill {script name}")
