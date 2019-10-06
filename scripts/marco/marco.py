import sys
sys.path.append(".") # Required for importing from parent relative path
import Larva
import utility

Larva.Log("polo").to_larva()
Larva.Log(sys.argv).to_larva()
