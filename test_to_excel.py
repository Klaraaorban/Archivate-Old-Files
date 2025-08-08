# i wanted to originally save the log to an excel file, but it was not working because of the pandas limitation on my work computer
import os
import datetime
from pathlib import Path
import shutil
import csv
# import pandas as pd

SOURCE_FOLDER = Path(r"give yours")
DESTINATION = Path(r"give yours")
AGE = 5
LOG_PATH = Path("archivation_log.csv")

DESTINATION.mkdir(exist_ok=True)

now = datetime.datetime.now()
minimal_age = now - datetime.timedelta(days=AGE*365)

col_names = ["original_path", "archived_path", "last_modified","archived_date", "size"]

log_rows = []

for file in SOURCE_FOLDER.rglob("*"):
    if file.is_file():
        last_mod_time = datetime.datetime.fromtimestamp(file.stat().st_mtime)

        if last_mod_time < minimal_age:
            relative_path = file.relative_to(SOURCE_FOLDER)
            target_path = DESTINATION / relative_path
            target_path.parent.mkdir(parents=True, exist_ok=True)
            size = file.stat().st_size
            last_modif_str = last_mod_time.strftime("%Y-%m-%d %H:%M:%S")
            archived_date = now.strftime("%Y-%m-%d %H:%M:%S")


            log_rows.append({
                "original_path": str(file),
                "archived_path": str(target_path),
                "last_modified": last_modif_str,
                "archived_date": archived_date,
                "size": size
            })

            shutil.move(str(file), str(target_path))
            print(f"Moved {file} to {target_path}")

if log_rows:
    df = pd.DataFrame(log_rows)
    df.to_excel(LOG_PATH, index=False)
    print(f"Log saved to {LOG_PATH.resolve()}")

print("Done scanning archives! All archives saved to archive folder")