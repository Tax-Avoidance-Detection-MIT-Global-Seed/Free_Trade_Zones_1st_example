from pathlib import Path
import os
from typing import List, Tuple

os.chdir(str((Path(__file__).resolve()).parent.parent))

import main


# Set to use the configuration file and output directory
args = [
    "-o",
    "tmp",
    "-f",
    "tests/configurations/zona_franca/zona_franca_simplecase_2.yml",
]

provisional = main.main(args)
