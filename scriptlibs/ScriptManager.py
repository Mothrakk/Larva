import utility
import scriptlibs.Script
import scriptlibs.ScriptList

class ScriptManager:
    def __init__(self) -> None:
        self.script_list = scriptlibs.ScriptList.ScriptList()
        self.scripts = [scriptlibs.Script.Script(p) for p in self.script_list.paths]
        for s in self.scripts:
            if s.name in self.read_autostart():
                s.start()

    def read_autostart(self) -> list:
        return utility.file_read(utility.pipe_path(".autostart")).strip().split("\n")

    def handle_kb_input(self, inp: str) -> None:
        if inp == "s":
            self.scripts[0].start()
        elif inp == "e":
            self.scripts[0].kill()
        elif inp == "poll":
            utility.write_to_larva(utility.build_log(self.scripts[0].p.pid, "Larva"))

    def handle_script_input(self) -> None:
        for line in utility.file_flush(utility.pipe_path("larva")).split("\n"):
            if line != "":
                print(line)
