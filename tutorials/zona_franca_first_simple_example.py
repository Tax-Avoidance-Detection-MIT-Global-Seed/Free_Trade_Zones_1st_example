from pathlib import Path
import sys
import os

parent_dir  = str((Path(__file__).resolve()).parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import main

os.chdir(parent_dir)

from util.plot_ipd import plot_iterated_prisoners_dilemma, plot_ipd_from_file
from fitness.game_theory_game import PrisonersDilemma
from typing import List, Tuple


# Set to use the configuration file and output directory
args = ["-o", "tmp", "-f", "tests/configurations/zona_franca/zona_franca_simple_first_example.yml"]
provisional = main.main(args)

