import sys
import time

import LarvaLibs.Utility as Utility

class Boilerplate:
    """Class meant for use by the subprocesses. Contains boilerplate functionality."""
    def __init__(self):
        self.name = sys.argv[0].split("\\")[-1].split(".")[0]
        self.larva_pid = sys.argv[1]
    
    def read_from_larva(self) -> list:
        """Check if there are new inputs from Larva.

        Returns a list where each element is a command (line) from Larva."""
        return Utility.file_flush(Utility.pipe_path(self.name))

    def tick(self) -> float:
        """Sleep for x seconds, returns x."""
        time.sleep(0.3)
        return 0.3

    def larva_alive(self) -> None:
        """Check if Larva is still alive. If not, kill the process."""
        if not Utility.pid_alive(self.larva_pid):
            exit(1)
