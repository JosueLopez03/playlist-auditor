import os
import sys
import re
from datetime import datetime
import unicodedata

def normalize_filename(filename: str) -> str:
    """
    Normalize a music filename:
    - lowercase
    - remove text in () and []
    - strip extension
    - normalize spacing and dashes
    """
    # Remove extension
    name, _ = os.path.splitext(filename)

    # Lowercase
    name = name.lower()

    # Remove parenthesis/brackets and their contents
    name = re.sub(r"\(.*?\)", "", name)   # remove ( ... )
    name = re.sub(r"\[.*?\]", "", name)   # remove [ ... ]

    # Collapse multiple spaces and normalize dash spacing
    name = re.sub(r"\s*-\s*", " - ", name)      # collapse any leftover
    name = re.sub(r"-{2,}", "-", name)          # replace multiple dashes with single dash
    name = re.sub(r"\s+", " ", name).strip()    # final trim

    name = unicodedata.normalize("NFC", name)
    return name

def normalize_music_folder(folder_path: str, dry_run: bool = True, log_file: str = "normalized_log.txt"):
    seen = set()
    log_entries = []

    for filename in list(os.listdir(folder_path)):
        if filename.lower().endswith(".ogg"):
            normalized_base = normalize_filename(filename)
            new_name = normalized_base + ".ogg"

            # Handle collisions
            counter = 1
            while new_name in seen or os.path.exists(os.path.join(folder_path, new_name)):
                new_name = f"{normalized_base}_{counter}.ogg"
                counter += 1

            seen.add(new_name)

            if filename != new_name:
                entry = f"{filename}  -->  {new_name}"
                print(entry)
                log_entries.append(entry)

                if not dry_run:
                    old_path = os.path.join(folder_path, filename)
                    new_path = os.path.join(folder_path, new_name)
                    try:
                        os.rename(old_path, new_path)
                    except FileNotFoundError:
                        print(f"File not found: {old_path}. Skipping.")
                    except Exception as e:
                        print(f"Error renaming {old_path}: {e}")

    if log_entries:
        with open(os.path.join(folder_path, log_file), "a", encoding="utf-8") as log:
            log.write(f"\n=== Normalization run on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            for entry in log_entries:
                log.write(entry + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 this_file.py /path/to/music/folder [--apply]")
        sys.exit(1)

    music_dir = os.path.expanduser(sys.argv[1])  # expand ~ to home dir
    dry_run = "--apply" not in sys.argv          # only rename if --apply is passed

    normalize_music_folder(music_dir, dry_run=dry_run)