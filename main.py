# main.py
import subprocess
import json
from tqdm import tqdm
import pandas as pd

results = {}
failed = []

coconut_filtered_df = pd.read_csv('/Users/student/database_filtering/Planning/coconut_purchasable_filtered.csv')
coconut_filtered_smi = dict(zip(coconut_filtered_df['identifier'], coconut_filtered_df['canonical_smiles']))


for k, smiles in tqdm(coconut_filtered_smi.items(), desc="Processing molecules"):
    try:
        proc = subprocess.run(
            ["python", "worker.py", smiles],
            capture_output=True,
            text=True,
            timeout=30  # optional but recommended
        )

        print("KEY:", k)
        print("RETURNCODE:", proc.returncode)
        print("STDOUT:", proc.stdout)
        print("STDERR:", proc.stderr)
        print("-" * 40)

        if proc.returncode != 0:
            # crash or controlled failure
            failed.append(k)
            results[k] = "failed"
            continue

        output = json.loads(proc.stdout)

        if output["status"] != "ok":
            failed.append(k)
            results[k] = "failed"
        else:
            results[k] = output["result"]

    except subprocess.TimeoutExpired:
        failed.append(k)
        results[k] = "timeout"

print("Done.")
print(f"Failed molecules: {len(failed)}")

with open('coconut_filtered_functional_groups.json', 'w') as f:
    json.dump(results, f)

with open('coconut_filtered_failed.txt', 'w') as f:
    for item in failed:
        f.write(f"{item}\n")