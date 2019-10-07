import sys
sys.path.append(".") # Required for importing from parent relative path

import LarvaLibs.Utility as Utility
from LarvaLibs.Log import Log

while Utility.tick():
    if not Utility.pid_alive(sys.argv[1]):
        exit(0)
    for line in Utility.file_flush(Utility.pipe_path("marco")):
        Log(line).to_larva()
