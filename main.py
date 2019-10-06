import msvcrt
import utility
import Larva

manager = Larva.Larva()

while utility.tick():
    if msvcrt.kbhit():
        manager.handle_kb_input(input(">"))
    manager.handle_scripts_input()
