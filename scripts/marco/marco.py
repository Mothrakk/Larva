import sys
sys.path.append(".") # Required for importing from parent relative path
from time import sleep

from LarvaLibs.Boilerplate import Boilerplate
from LarvaLibs.Log import Log

boiler = Boilerplate()

Log(" ".join(boiler.real_args)).to_larva()
