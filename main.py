import msvcrt

import utility
import scriptlibs.ScriptManager

larva = scriptlibs.ScriptManager.ScriptManager()

while utility.tick():
    if msvcrt.kbhit():
        larva.handle_kb_input(input(">"))
    larva.handle_script_input()
