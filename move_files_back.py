# this is a backuplan--if you decide to move files back to their original places

# possible error: archivation_log.csv not found(path error)
import csv
from pathlib import Path
import shutil

LOG_PATH = Path(r"archivation_log.csv")

with LOG_PATH.open("r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        archived = Path(row["archived_path"])
        original = Path(row["original_path"])

        if archived.exists():
            original.parent.mkdir(parents=True, exist_ok=True)

            try:
                shutil.move(str(archived), str(original))
                print(f"Moved {archived} to {original}  -- original place")
            except Exception as e:
                print(f"Failed move {archived} to {original} -- {e}")
        else:
            print(f"Archived file not found: {archived}")

print("Vertig")