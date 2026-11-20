import sys
import os
import zipfile

print("Extracting APK files...")

apk_path = sys.argv[1]
output_path = sys.argv[2]

with zipfile.ZipFile(apk_path, "r") as apk:
    apk.extractall(output_path)
os.remove(apk_path)

print()
print(f"Extracted {apk_path} to {output_path}")
