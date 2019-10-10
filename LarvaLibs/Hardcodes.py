import subprocess
import random
import os

import LarvaLibs.Utility as Utility
from LarvaLibs.Script import Script

class Hardcodes:
    def __init__(self, larva):
        self.larva = larva
        self.d = {
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

    def help(self, inp: list) -> None:
        print(f"cmds: {'; '.join(self.d.keys())}")
        print(f"scripts: {'; '.join(self.larva.scripts.keys())}")
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
            if inp[1] in self.larva.scripts:
                print(f"Configuring new cfg file for {inp[1]}")
                new_cfg = []
                for key in Script.REQUIRED_CFG_SETTINGS:
                    while True:
                        v = input(f"Select value for {key} {Script.REQUIRED_CFG_SETTINGS[key]}: ")
                        if v in Script.REQUIRED_CFG_SETTINGS[key]:
                            new_cfg.append(f"{key}:{v}")
                            break
                        print(f"Value must be in {Script.REQUIRED_CFG_SETTINGS[key]}")
                Utility.file_write(self.larva.scripts[inp[1]].cfg_path, "\n".join(new_cfg))
            else:
                print(f"{inp[1]} not found")

    def start(self, inp: list) -> None:
        if len(inp) > 1:
            if inp[1] in self.larva.scripts:
                self.larva.scripts[inp[1]].proc_start(inp[2:])
            else:
                print(f"{inp[1]} not found")
        else:
            print("start {script name} {arg} {arg} ...")

    def kill(self, inp: list) -> None:
        if len(inp) == 1:
            if input("Exit Larva? (Y)").lower() == "y":
                exit(0)
        elif inp[1] in self.larva.scripts:
            self.larva.scripts[inp[1]].kill()

    def e(self, inp: list) -> None:
        exit(0)

    def greet(self, inp: list) -> None:
        filename = random.choice(os.listdir("logos"))
        with open(f"logos\\{filename}", "r") as fptr:
            print(fptr.read())

    def man(self, inp: list) -> None:
        if len(inp) == 1:
            print(r"man {cmd}")
        elif inp[1] not in self.d:
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
