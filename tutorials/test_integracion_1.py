from pathlib import Path
import sys
import os

parent_dir  = str((Path(__file__).resolve()).parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import main

os.chdir(parent_dir)

# Set to use the configuration file and output directory
args = [
    "-o",
    "tmp",
    "-f",
    "tests/configurations/zona_franca/zona_franca_simplecase_2.yml",
]

provisional = main.main(args)
