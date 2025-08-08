# this python script gets as input a source folder, a destination folder and an age in years
# using these inputs, the code looks through the files and moves the files older than the specified age to the destination folder
# it also creates a log file with the original path, archived path, last modified date - so that the files can be moved back if needed and manual verification can be done

# possible error: paths don't match, don't exist, no permission OR the \ is accidentally written as / in the path

# changes can be made to the numbered comment sections
import os
import datetime
from pathlib import Path
import shutil
import csv

# 1. change the folder path to the folder you want to archive:   Path(r"xzyz\xyz\xyz")
SOURCE_FOLDER = Path(r"C:\Users\klara.orban\OneDrive - Reformierte Kirchen Bern Jura Solothurn\Dokumente\Programming\Archivate Old Files\test_dataset")

# 2. change the destination folder path to the folder you want to archive to:   Path(r"xzyz\xyz\xyz")
DESTINATION = Path(r"C:\Users\klara.orban\OneDrive - Reformierte Kirchen Bern Jura Solothurn\Dokumente\Programming\Archived")

# 3. change the age in years to the age you want to archive files older than
AGE = 5

# 4. this is the logs file where the original path, archived path, last modified date and archived date will be saved
LOG_PATH = Path("archivation_log.csv")


DESTINATION.mkdir(exist_ok=True)

now = datetime.datetime.now()
minimal_age = now - datetime.timedelta(days=AGE*365)

col_names = ["original_path", "archived_path", "last_modified","archived_date", "size"]

log = LOG_PATH.exists()
log_file = LOG_PATH.open("a", newline='', encoding='utf-8')
csv_writer = csv.DictWriter(log_file, fieldnames=col_names)
if not log:
    csv_writer.writeheader()



for file in SOURCE_FOLDER.rglob("*"):
    if file.is_file():
        last_mod_time = datetime.datetime.fromtimestamp(file.stat().st_mtime)

        if last_mod_time < minimal_age:
            relative_path = file.relative_to(SOURCE_FOLDER)
            target_path = DESTINATION / relative_path
            target_path.parent.mkdir(parents=True, exist_ok=True)
            size = file.stat().st_size
            last_modif_2 = last_mod_time.strftime("%Y-%m-%d %H:%M:%S")
            archived_date = now.strftime("%Y-%m-%d %H:%M:%S")


            csv_writer.writerow({
                "original_path": str(file),
                "archived_path": str(target_path),
                "last_modified": last_modif_2,
                "archived_date": archived_date,
                "size": size
            })

            shutil.move(str(file), str(target_path))
            print(f"Moved {file} to {target_path}")
        

log_file.close()
print("Done scanning archives! All archives saved to archive folder")
