# IMPORTS
import os
import sys
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from pathlib import Path
import shutil

TEXT_FILE_EXTENSIONS = ('.csv', '.imgcut', '.mamodel', '.maanim')
EN_PACK_KEY = bytes.fromhex("0ad39e4aeaf55aa717feb1825edef521")
EN_PACK_IV = bytes.fromhex("d1d7e708091941d90cdf8aa5f30bb0c2")

LANGUAGES = ("de", "es", "fr", "it", "th")


# FUNTIONS
def decrypt_list(list_path) -> str:

    key = hashlib.md5(b"pack").hexdigest()[:16].encode("utf-8")
    cipher = AES.new(key, AES.MODE_ECB)

    with open(list_path, "rb") as list_file:
        encrypted_data = list_file.read()

    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    return decrypted_data.decode("utf-8")


def decrypt_pack(list_text: str, pack_path, output_path) -> None:
    lines = list_text.strip().splitlines()

    pack_name = os.path.basename(pack_path).lower()
    is_image_data_pack = "imagedatalocal" in pack_name
    is_server_pack = "server" in pack_name
    if is_server_pack:
        key = hashlib.md5(b"battlecats").hexdigest()[:16].encode("ascii")
        mode = AES.MODE_ECB
    else:
        key = EN_PACK_KEY
        mode = AES.MODE_CBC

    with open(pack_path, "rb") as pack_file:
        for line in lines[1:]:
            parts = line.split(",")
            if len(parts) != 3:
                continue
            filename, offset, size = parts[0], int(parts[1]), int(parts[2])
            pack_file.seek(offset)
            chunk = pack_file.read(size)
            full_output_path = os.path.join(output_path, filename)
            if is_image_data_pack:
                decrypted_chunk = chunk
            else:
                try:
                    if mode == AES.MODE_CBC:
                        cipher = AES.new(key, mode, iv=EN_PACK_IV)
                    else:
                        cipher = AES.new(key, mode)
                    decrypted_chunk = unpad(cipher.decrypt(chunk), AES.block_size)
                    if filename.endswith(TEXT_FILE_EXTENSIONS):
                        decrypted_chunk.decode("utf-8")
                except (ValueError, UnicodeDecodeError) as exc:
                    print(f"[Warning] Could not decrypt {filename} in {os.path.basename(pack_path)}: {exc}")
                    continue

            with open(full_output_path, "wb") as output_file:
                output_file.write(decrypted_chunk)

def find_output_path(pack_name: str, out_folder: Path) -> Path:
    family = Path(pack_name).stem
    language = None

    for code in LANGUAGES:
        suffix = f"_{code}"
        if family.endswith(suffix):
            family = family[:-len(suffix)]
            language = code
            break

    if family == "DataLocal":
        return out_folder/"DataLocal"
    if family == "resLocal":
        return out_folder/"resLocal"/(language or "en")
    if family == "ImageLocal" or family == "ImageDataLocal":
        return out_folder/"images"/(language or "en")
    else:
        return out_folder/"other"/family/(language or "en")

def find_png_path(pack_name, out_folder: Path) -> Path:
    LANGUAGES = ("de", "es", "fr", "it", "th", "en")
    family = Path(pack_name).stem
    language = None

    for code in LANGUAGES:
        suffix = f"_{code}"
        if family.endswith(suffix):
            family = family[:-len(suffix)]
            language = code

    return out_folder/"images"/(language or "")

# PROGRAM
def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("ERROR: decrypt.py <version>")

    version_number = sys.argv[1]
    out_folder = Path(f"./game_data/en/v{version_number}")
    assets_folder = Path(f"./apks/en/v{version_number}/assets")

    lists_count = 0
    packs_count = 0
    print("Decrypting packs...")
    print("")
    for list_path in assets_folder.rglob("*.list"):
        lists_count += 1
        for pack_path in assets_folder.rglob(f"{list_path.stem}.pack"):
            output_path = find_output_path(pack_path.stem, out_folder)
            decrypt_pack(decrypt_list(list_path), pack_path, output_path)

            packs_count += 1


    print(f"Total lists found and decrypted: {str(lists_count)}")
    print(f"Total packs found and decrypted: {str(packs_count)}")

    png_count = 0
    print("Copying images...")
    for png_file in assets_folder.rglob("*.png"):
        shutil.copy(png_file, find_png_path(png_file, out_folder))
        png_count += 1

    print(f"Total images copied : {str(png_count)}")



if __name__ == "__main__":
    main()
