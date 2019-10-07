import msvcrt

import LarvaLibs.Utility as Utility
from LarvaLibs.Larva import Larva

manager = Larva()

while manager.tick():
    if msvcrt.kbhit():
        manager.handle_kb_input(input(">"))
    manager.handle_scripts_input()
