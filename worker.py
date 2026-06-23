import os

os.chdir('efgs_test')


from rdkit import Chem
from rdkit.Chem.Draw import IPythonConsole
#from chembl_structure_pipeline import standardizer as sdz
from datetime import datetime
from IPython.display import Image
from PIL import Image as pilImage
from PIL import ImageDraw, ImageFont
from rdkit.Chem.Draw import rdMolDraw2D
import pandas as pd
import io
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
EFGS_DIR = os.path.join(HERE, "efgs_test")
sys.path.insert(0, EFGS_DIR)
from efgs import get_dec_fgs

def main():
    if len(sys.argv) != 2:
        print(json.dumps({"status": "error", "reason": "No SMILES provided"}))
        sys.exit(1)

    smiles = sys.argv[1]

    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError("Invalid SMILES")

        result = get_dec_fgs(mol)

        # IMPORTANT: only return JSON-serializable data
        output = {
            "status": "ok",
            "result": result[2]  # psmis, or whatever you need
        }

        print(json.dumps(output))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({
            "status": "failed",
            "error": str(e)
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
