import gzip
import pathlib
import sys
import fnmatch

conversions = {
    "Guitar Rig 5": "Guitar Rig 6",
    "Guitar%20Rig%205": "Guitar%20Rig%206",
    "1315522357": "1315513426"
}

def convert(infile):
    with gzip.open(infile, 'rb') as f_in:
        full_text = f_in.read().decode()
        for old, new in conversions.items():
            full_text=full_text.replace(old, new)
    with gzip.open(infile, "wb") as f_out:
        f_out.write(full_text.encode())

def recursive_search(dirpath, target_filetype="*.als", callback=convert):
    found_files = []
    for file in pathlib.Path(dirpath).iterdir():
        # print("cecking", file)
        if file.is_dir():
            found_files += recursive_search(file, target_filetype)
        elif fnmatch.fnmatch(file.name, target_filetype):
            print("Converting:",file )
            callback(file)
            found_files += [file]
    return found_files

if __name__ == "__main__":
    recursive_search(sys.argv[1])