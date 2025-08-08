# this script creates a fake dataset with specific files and modification times to test the archiving script
import os
import datetime
from pathlib import Path

base_folder = Path("test_dataset")
base_folder.mkdir(exist_ok=True)

subfolders = ["docs", "images", "data"]
for sf in subfolders:
    (base_folder / sf).mkdir(exist_ok=True)

file_specs = [
    ("docs/report2_2015.txt", "Old repofsrt from 2015", -365*9),  # 9 years old
    ("docs/report2313_2020.txt", "Repodrt from 2020", -365*4),
    ("images/phot4o_2016.jpg", "Fake p3hoto", -365*8),
    ("images/photggfdo_2024.jpg", "New3 photo", -30),
    ("data/datfgda_2017.csv", "Some C3SV data", -365*7),
    ("data/datad_2025.csv", "Recent wCSV data", -5),
]

for rel_path, content, days_old in file_specs:
    file_path = base_folder / rel_path
    file_path.write_text(content)

    old_time = datetime.datetime.now() + datetime.timedelta(days=days_old)
    mod_time = old_time.timestamp()
    os.utime(file_path, (mod_time, mod_time))

print(f"Fake dataset updated in: {base_folder.resolve()}")
