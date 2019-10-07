import sys
sys.path.append(".") # Required for importing from parent relative path

from LarvaLibs.Boilerplate import Boilerplate
from LarvaLibs.Log import Log

boiler = Boilerplate()

Log(" ".join(sys.argv[2:])).to_larva()

