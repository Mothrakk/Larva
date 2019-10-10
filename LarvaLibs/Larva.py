import os
import subprocess
import time
import random

import LarvaLibs.Utility as Utility
from LarvaLibs.Script import Script

class Larva:
    def __init__(self):
        self.clear(None)
        self.HARDCOMMANDS = {
            "help" :self.help,
            "shell":self.shell,
            "cls"  :self.clear,
            "recfg":self.recfg,
            "start":self.start,
            "e"    :self.e,
            "man"  :self.man,
            "greet":self.greet,
            "kill" :self.kill
        }
        self.create_missing_folders()
        self.scripts = self.build_scripts_dict()
        self.handle_autostart_scripts()
        self.help(None)

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
        else:
            print(f"Unknown command: {inp[0]}, try running 'help'")

    def check_scripts_pulse(self) -> None:
        pass

    def help(self, inp: list) -> None:
        print(f"cmds: {'; '.join(self.HARDCOMMANDS.keys())}")
        print(f"scripts: {'; '.join(self.scripts.keys())}")
        print("Use 'man' for more specific documentation.")

    def shell(self, inp: list) -> None:
        if len(inp) == 1:
            print(r"shell {arg} {arg} ...")
        else:
            subprocess.run(" ".join(inp[1:]), shell=True)

    def clear(self, inp: list) -> None:
        subprocess.run("cls", shell=True)
        self.greet(inp)

    def recfg(self, inp: list) -> None:
        if len(inp) == 1:
            print("recfg {script name}")
        else:
            if inp[1] in self.scripts:
                print(f"Configuring new cfg file for {inp[1]}")
                new_cfg = []
                for key in Script.REQUIRED_CFG_SETTINGS:
                    while True:
                        v = input(f"Select value for {key} {Script.REQUIRED_CFG_SETTINGS[key]}: ")
                        if v in Script.REQUIRED_CFG_SETTINGS[key]:
                            new_cfg.append(f"{key}:{v}")
                            break
                        print(f"Value must be in {Script.REQUIRED_CFG_SETTINGS[key]}")
                Utility.file_write(self.scripts[inp[1]].cfg_path, "\n".join(new_cfg))
            else:
                print(f"{inp[1]} not found")

    def start(self, inp: list) -> None:
        if len(inp) > 1:
            if inp[1] in self.scripts:
                self.scripts[inp[1]].proc_start(inp[2:])
            else:
                print(f"{inp[1]} not found")
        else:
            print("start {script name} {arg} {arg} ...")

    def kill(self, inp: list) -> None:
        if len(inp) == 1:
            if input("Exit Larva? (Y)").lower() == "y":
                exit(0)
        elif inp[1] in self.scripts:
            self.scripts[inp[1]].kill()

    def e(self, inp: list) -> None:
        exit(0)

    def greet(self, inp: list) -> None:
        filename = random.choice(os.listdir("logos"))
        with open(f"logos\\{filename}", "r") as fptr:
            print(fptr.read())

    def man(self, inp: list) -> None:
        if len(inp) == 1:
            print(r"man {cmd}")
        elif inp[1] not in self.HARDCOMMANDS:
            print(f"{inp[1]} not found")
        else:
            print(
                {
                    "help" :"""Lists out the available hardcoded commands (cmds) and the scripts that have been loaded in (scripts).""",
                    "shell":"""Run arguments straight into the terminal/shell and see what happens. Stdout visible.
Ex: 'shell TASKLIST /FO LIST /FI "IMAGENAME eq python.exe"'""",
                    "cls"  :"""Shortcut for 'shell cls' into `greet`""",
                    "recfg":"""Allows for creating a cfg file for a script if one happens to be corrupted or missing.""",
                    "start":"""Attempt to start a given script if it isn't running already.""",
                    "kill" :"""Attempt to kill a given running script.
Running this with no arguments prompts you with the possibility to kill Larva. Same as 'e'.""",
                    "e"    :"""Kill Larva 'safely'.""",
                    "greet":"""Print out one of the logos from the 'logos' folder.""",
                    "man"  :"""Meta. Read a script's more specific documentation."""
                    }[inp[1]])
