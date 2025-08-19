"""
tets_CalcF1Score.py
"""

import runpy, sys
from pathlib import Path
from unittest.mock import patch

def test_calcf1_path(tmp_path):
    """
    Runs CalcF1Score.py without changing it. Mocks the pharmit call without the need for a real database.

    Verifies F1/Recall/Precision/HitRate/EF.
    """

    # 1. Prepare actives and decoys
    actives = tmp_path/"actives.ism"
    decoys = tmp_path/"decoys.ism"
    actives.write_text("A\nB\nC\n")
    decoys.write_text("D\nE\n")

    # 2. Dummy query file 
    query = tmp_path / "Top5.json"
    query.write_text("{}\n")
