import os

class ScriptList:
    def __init__(self) -> None:
        self.seek_script_paths()

    def seek_script_paths(self) -> None:
        self.paths = []
        for x in os.listdir("scripts"):
            if len(x.split(".")) == 2:
                if x[-2:] == "py":
                    self.paths.append(f"scripts\\{x}")
            else:
                self.paths.append(f"scripts\\{x}\\{x}.py")
