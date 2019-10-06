import sys
sys.path.append(".") # Required for importing from parent relative path
import Larva
import utility

while utility.tick():
    for line in utility.file_flush(utility.pipe_path("marco")):
        Larva.Log(line).to_larva()
