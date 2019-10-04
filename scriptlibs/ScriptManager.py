import subprocess
import utility
import scriptlibs.Script
import scriptlibs.ScriptList

class ScriptManager:
    def __init__(self) -> None:
        self.HARDCOMMANDS = {
            "exit":self.kill,
            "help":self.help,
            "cls":self.clear
        }
        self.script_list = scriptlibs.ScriptList.ScriptList()
        self.scripts = [scriptlibs.Script.Script(p) for p in self.script_list.paths]
        for s in self.scripts:
            if s.name in self.read_autostart():
                s.start()

    def read_autostart(self) -> list:
        return utility.file_read(utility.pipe_path(".autostart")).strip().split("\n")

    def handle_kb_input(self, inp: str) -> None:
        inp = inp.strip().split(" ")
        if inp[0] in self.HARDCOMMANDS:
            self.HARDCOMMANDS[inp[0]](inp)

    def handle_script_input(self) -> None:
        for line in utility.file_flush(utility.pipe_path("larva")).split("\n"):
            if line != "":
                print(line)

    def help(self, *argv: list) -> str:
        utility.write_to_larva(utility.build_log("; ".join(self.HARDCOMMANDS.keys())))

    def kill(self, *argv: list) -> None:
        for s in self.scripts:
            s.kill()
        utility.write_to_larva(utility.build_log("Exiting"))
        self.handle_script_input()
        exit(0)

    def clear(self, *argv: list) -> None:
        subprocess.run("cls", shell=True)
