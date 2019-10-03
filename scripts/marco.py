import os
import sys
sys.path.append(".")

import utility

my_name = utility.my_name()

utility.write_to_larva(utility.build_log(sys.argv[0], my_name))
